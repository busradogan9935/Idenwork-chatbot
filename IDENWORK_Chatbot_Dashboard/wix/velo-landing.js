// Wix Velo sayfa kodu. Wix Editöründe şu ID'leri oluşturun:
// #mesajInput, #sorButton, #cevapText, #isimInput, #telefonInput, #leadMesajInput,
// #onayCheckbox, #kaydetButton, #durumText
// API_URL'yi kendi Render adresinizle değiştirin. Ziyaretçiye özel geçmiş bu temel örnekte yoktur.
import {fetch} from 'wix-fetch';
const API_URL = 'https://YOUR-RENDER-APP.onrender.com';
$w.onReady(function () {
  $w('#sorButton').onClick(async () => {
    try {
      const res = await fetch(`${API_URL}/api/sohbet`, {method:'post',headers:{'Content-Type':'application/json'},body:JSON.stringify({mesaj:$w('#mesajInput').value,gecmis:[]})});
      const data = await res.json();
      $w('#cevapText').text = data.basari ? data.cevap : data.hata;
    } catch (err) { $w('#cevapText').text = 'Şu anda bağlantı kurulamadı.'; }
  });
  $w('#kaydetButton').onClick(async () => {
    try {
      const res = await fetch(`${API_URL}/api/leads`, {method:'post',headers:{'Content-Type':'application/json'},body:JSON.stringify({isim:$w('#isimInput').value,telefon:$w('#telefonInput').value,mesaj:$w('#leadMesajInput').value,onay:$w('#onayCheckbox').checked})});
      const data = await res.json();
      $w('#durumText').text = data.basari ? 'Kaydınız alındı.' : data.hata;
    } catch (err) { $w('#durumText').text = 'Bağlantı hatası.'; }
  });
});
