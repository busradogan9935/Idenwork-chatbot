"""Bağımsız yapay zekâ katmanı. Flask/SQL kullanılmaz."""
import os
import requests
from config import BUSINESS_CONTEXT

class AIServiceError(Exception):
    pass

class AIService:
    def _sistem_talimati(self):
        return os.environ.get('BUSINESS_CONTEXT', BUSINESS_CONTEXT)

    def _groq_istegi(self, mesaj, gecmis):
        api_key = os.environ.get('GROQ_API_KEY', '')
        if not api_key:
            return None
        temiz_gecmis = [m for m in gecmis[-10:] if isinstance(m, dict) and m.get('role') in ('user','assistant') and isinstance(m.get('content'),str)]
        messages = [{'role':'system','content':self._sistem_talimati()}] + temiz_gecmis + [{'role':'user','content':mesaj}]
        try:
            r = requests.post('https://api.groq.com/openai/v1/chat/completions',
                headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'},
                json={'model':'llama-3.1-8b-instant','messages':messages,'temperature':0.65,'max_tokens':450}, timeout=25)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIServiceError('Yapay zekâ servisine şu anda ulaşılamıyor.') from exc

    def yanit_uret(self, mesaj, gecmis=None):
        gecmis = gecmis or []
        if os.environ.get('AI_PROVIDER', 'groq') != 'groq':
            raise AIServiceError('Seçilen yapay zekâ sağlayıcısı desteklenmiyor.')
        cevap = self._groq_istegi(mesaj, gecmis)
        if cevap:
            return cevap
        return ('Demo modu: Paylaştığın deneyimde seni en çok zorlayan durum neydi? '
                'Connect · Align · Act ile önce yaşadığın olayı, sonra senin için önemli olan değerleri '
                've deneyebileceğin küçük bir adımı birlikte keşfedebiliriz. '
                '(Gerçek AI için GROQ_API_KEY eklenmelidir.)')

ai_service = AIService()
