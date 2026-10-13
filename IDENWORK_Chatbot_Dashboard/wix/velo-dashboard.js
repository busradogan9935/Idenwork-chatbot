// Wix yönetim sayfasındaki repeater #leadRepeater, içindeki metinler #isimText,
// #telefonText, #mesajText, #tarihText. DİKKAT: /api/leads oturumla korunur;
// Wix cross-domain paneli güvenli kullanmak için Wix backend proxy + yetki kontrolü gerekir.
// Bu örnek veri bağlama gösterimidir, üretimde doğrudan çalışmaz.
// Yerleşik güvenli yönetim panelini kullanın: https://YOUR-RENDER-APP.onrender.com/dashboard
// $w('#leadRepeater').data = leads.map(item => ({...item, _id: String(item.id)}));
// $w('#leadRepeater').onItemReady(($item, itemData) => {
//   $item('#isimText').text = itemData.isim;
//   $item('#telefonText').text = itemData.telefon;
//   $item('#mesajText').text = itemData.mesaj || '';
//   $item('#tarihText').text = itemData.tarih;
// });
