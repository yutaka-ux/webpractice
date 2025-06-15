(function () {
    var topBtn = ('#page-top');
    topBtn.hide();
    (window).scroll(function () {
        if ((this).scrollTop() > 100) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
    });
    topBtn.click(function () {
        ('body,html').animate({
            scrollTop: 0
        }, 500);
        return false;
    });
});

(function () {
    ('a[href^=#]').click(function () {
        var speed = 500;
        var href = (this).attr("href");
        var target = (href == "#" || href == "" ? 'html' : href);
        var position = target.offset().top;
        ("html, body").animate({ scrollTop: position }, speed, "swing"); return false;
    });
});


(function () {
    ('.global-navi li a').each(function () {
        var href = (this).attr('href');
        if (location.href.match(href)) {
            (this).addClass('active');
        } else {
            (this).removeClass('active');
        }
    });
});

(function () {
    ('.tabbox:first').show();
    ('#tab li:first').addClass('active');
    ('#tab li').click(function () {
        ('#tab li').removeClass('active');
        (this).addClass('active');
        ('.tabbox').hide();
        ((this).find('a').attr('href')).fadeIn();
        return false;
    });
});


(function () {
    (".pointimgbox li a ,.setsubiright a img,.contactArea a img").hover(function () {
        (this).fadeTo("4000", 0.7);
    }, function () {
        (this).fadeTo("4000", 1.0);
    });
});


////////////////ハンバーガーメニュー
document.addEventListener('DOMContentLoaded', function () {
    // 既存のJavaScriptコードがあれば、その下に追加してください

    const hamburgerButton = document.querySelector('.hamburger-menu-button');
    const mobileNav = document.getElementById('global-navi-mobile');
    const body = document.body; // body要素を取得

    if (hamburgerButton && mobileNav) { // 要素が存在するか確認
        hamburgerButton.addEventListener('click', function () {
            // is-active クラスをトグルする
            hamburgerButton.classList.toggle('is-active');
            mobileNav.classList.toggle('is-active');

            // aria-expanded 属性をトグルする (アクセシビリティ対応)
            const isExpanded = hamburgerButton.getAttribute('aria-expanded') === 'true';
            hamburgerButton.setAttribute('aria-expanded', !isExpanded);

            // aria-hidden 属性をトグルする (アクセシビリティ対応)
            mobileNav.setAttribute('aria-hidden', isExpanded); // isExpandedの逆を設定

            // メニューが開いているときはbodyのスクロールを無効にする
            if (mobileNav.classList.contains('is-active')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = ''; // スクロールを元に戻す
            }
        });

        // モバイルナビゲーション内のリンクがクリックされたらメニューを閉じる
        const mobileNavLinks = mobileNav.querySelectorAll('a');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', function () {
                hamburgerButton.classList.remove('is-active');
                mobileNav.classList.remove('is-active');
                hamburgerButton.setAttribute('aria-expanded', 'false');
                mobileNav.setAttribute('aria-hidden', 'true');
                body.style.overflow = '';
            });
        });
    }
});
