var menuBar = document.querySelector('#menu_bar');
var navLinks = document.querySelector('.nav-links');





// navLinks.computedStyleMap.top='-450px'

if (menuBar && navLinks) {
    navLinks.style.top = '-450px';

    menuBar.onclick = function () {
        if (navLinks.style.top === '-450px') {
            navLinks.style.top = '50px';
        } else {
            navLinks.style.top = '-450px';
        }
    };
}

// !!KULLANICI BİLGİLENSİN DİYE!!

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("iletisimForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();                      // Sayfa yenilenmesin diye.
            alert("Mesaj başarıyla gönderildi!"); // Kullanıcıya bilgilendirmek için.
            form.reset();                           // Formu temizlemek
        });
    } else {
        console.log("Form bulunamadı!");
    }
});

// !! HOŞGELDİNİZ MESAJI!!

window.onload = () => {
    alert("Web sitemize hoş geldiniz!");
  };


// !!  DEĞİŞEN ARKA PLANLAR!!

const arkaPlanResimleri = [
    'images/13.jpeg',
    'images/sae.jpg',
    'images/hjk.jpeg'
  ];
  
  function rastgeleArkaPlanDegistir() {
    const rastgeleIndex = Math.floor(Math.random() * arkaPlanResimleri.length);
    document.body.style.backgroundImage = `url('${arkaPlanResimleri[rastgeleIndex]}')`;
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundRepeat = "no-repeat";
    document.body.style.backgroundAttachment = "fixed";
  }
  
  window.onload = rastgeleArkaPlanDegistir;
  setInterval(rastgeleArkaPlanDegistir, 10000);
  
// tekrar etsin ms'de.

// !!YUKARI BUTONU!!


document.addEventListener("DOMContentLoaded", function () {
    const yukariBtn = document.getElementById("yukariBtn");
    if (yukariBtn) {
      yukariBtn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
  
});





// !!ASAGI BUTONU!!


  document.addEventListener("DOMContentLoaded", function () {
    const asagiBtn = document.getElementById("asagiBtn");
    if (asagiBtn) {
      asagiBtn.addEventListener("click", function () {
        window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
      });
    }
  });
  


// !!MESAJ AT'A TIKLAYINCA UYGULAMAYA YÖNLENDİRSİN KISMI!!

  document.addEventListener("DOMContentLoaded", function () {
    const mesajBtn = document.getElementById("mesajBtn");
    mesajBtn.onclick = () => {
      window.location.href = "mailto:dragon_yazılım@gmail.com?subject=Merhaba&body  "; 
    };
  });
  
// !!!KULLANICI KAÇ KEZ TIKLADI KISMI!!!
  let sayac = 0;
  document.onclick = () => {
    sayac++;
    console.log("Tıklama: " + sayac);
  };
  

// !!KOPYALAMAYI ENGELLE!!
 document.addEventListener('copy', function (e) {
  e.preventDefault();
  alert("Kopyalama işlemi devre dışı bırakıldı!");
});


// !!SEÇMEYİ ENGELLE!!
document.addEventListener('selectstart', function (e) {
  e.preventDefault();
});



//  !SEÇTİĞİNDE UYARI VERSİN!!
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener('copy', function (e) {
    e.preventDefault();
    alert("Kopyalama işlemi devre dışı bırakıldı!");
  });
});



// ORTADAKİNİ YORUM SATIRI HALİNE GETİRİNCE ÇALIŞTI.


