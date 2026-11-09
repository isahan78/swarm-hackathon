"""Small optional train-only linear activation probe; no model hooks or pickle loads."""
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


class ActivationProbe:
    def __init__(self, seed=0, base_dir='.'):
        self.base_dir = Path(base_dir)
        self.pipeline = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, random_state=seed))
        self.signature = None

    def _features(self, rows, fit=False):
        vectors = []
        signature = self.signature
        for row in rows:
            meta = row.get('activation_metadata') or row.get('metadata', {}).get('activation', {})
            timing = meta.get('timing')
            if timing not in {'pre_response_context', 'pre_response'}:
                raise ValueError(f'Activation probe requires strict pre-response samples, got {timing!r}')
            if meta.get('layer') is None or meta.get('token_position') is None:
                raise ValueError('Activation extraction requires documented nonnull layer and token_position')
            for identity_key in ('episode_id', 'agent_id', 'target_step'):
                if identity_key in meta and meta[identity_key] != row.get(identity_key):
                    raise ValueError(f'Activation identity mismatch for {identity_key}')
                if row.get('backend_kind') == 'qwen' and meta.get(identity_key) is None:
                    raise ValueError(f'Qwen activation requires {identity_key} identity metadata')
            path = Path(row['activation_ref'])
            if not path.is_absolute():
                path = self.base_dir / path
            array = np.load(path, allow_pickle=False)
            if array.ndim != 1 or not np.isfinite(array).all():
                raise ValueError('Each activation must be a finite one-dimensional vector')
            inference = row.get('inference_metadata') or {}
            current = (row.get('model_id'), timing, meta.get('layer'), meta.get('token_position'), len(array),
                       inference.get('resolved_revision'), inference.get('chat_template_sha256'))
            if signature is None:
                signature = current
            if current != signature:
                raise ValueError(f'Mixed activation extraction signatures: {current!r} != {signature!r}')
            vectors.append(array)
        if fit:
            self.signature = signature
        return np.stack(vectors)

    def fit(self, rows):
        labels = [int(r['eventual_unauthorized_attempt']) for r in rows]
        if len(set(labels)) != 2:
            raise ValueError('Activation probe requires both outcome classes in training data')
        self.pipeline.fit(self._features(rows, fit=True), labels)
        return self

    def predict(self, rows):
        return self.pipeline.predict_proba(self._features(rows))[:, 1]
