(function() {
    void
    function() {
        function e(e, t) {
            function n(e, t) {
                r.push(encodeURIComponent(e) + "=" + encodeURIComponent(t))
            }
            if (!e) return;
            var r = [],
                t = t || {};
            for (var i in t) {
                if (e == "qqweibo" && i == "pic") {
                    r.push(i + "=" + decodeURIComponent(t[i]));
                    continue
                }
                n(i, t[i])
            }
            var s;
            switch (e) {
                case "sina":
                    s = "http://service.weibo.com/share/share.php?ralateUid=2615010375&";
                    break;
                case "qqzone":
                    s = "http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?";
                    break;
                case "renren":
                    s = "http://widget.renren.com/dialog/share?";
                    break;
                case "qqweibo":
                    s = "http://share.v.t.qq.com/index.php?c=share&a=index&"
            }
            var o = s + r.join("&");
            return o
        }
        function t(e) {
            var t = {
                url: shareUrl,
                pic: e,
                title: title
            }, n = {
                title: title,
                summary: content,
                desc: msg,
                url: shareUrl,
                pics: e
            };

            return renren = {
                title: title,
                resourceUrl: shareUrl,
                content: content,
                message: msg,
                pic: e
            }, qqweibo = {
                title: content,
                url: shareUrl,
                pic: e
            }, {
                sina: t,
                qqzone: n,
                renren: renren,
                qqweibo: qqweibo
            }
        }
        function n(n) {
            var r = $(".share"),
                i = t(n);
                r.find(".sina-weibo").attr("href", e("sina", i.sina));
                r.find(".qzone").attr("href", e("qqzone", i.qqzone));
                r.find(".qq-weibo").attr("href", e("qqweibo", i.qqweibo));
                r.find(".renren").attr("href", e("renren", i.renren));
        }
        n(shareImage)
    }()
})();