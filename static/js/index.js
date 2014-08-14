(function (){
    var page = 2;

    var articleTpl = [];

    articleTpl.push('<article class="container joke-item">');
    articleTpl.push('<span><a href="/detail/{$id}">{$title}</a></span>');
    articleTpl.push('<a href="/detail/{$id}">');
    articleTpl.push('<div class="content">');
    articleTpl.push('{$msg}');
    articleTpl.push('</div>');
    articleTpl.push('</a>');
    articleTpl.push('</article>');

    var reqData = function (p , callback , failCallback){
        $.ajax({
            url : "/joke/list/" + p , 
            type : "GET" ,
            success : callback ,
            failed : failCallback
        });
    };

    var buildArticle = function (data){
        var html = [];

        var _buildArticle = function (node){
            return articleTpl.join("")
                             .replace(/{\$id}/g , node.pk)
                             .replace(/{\$msg}/g , node.fields.msg)
                             .replace(/{\$title}/g , node.fields.title)
        }

        data = JSON.parse(data);
        data.forEach(function (el){
            html.push(_buildArticle(el));
        });

        return html.join("");
    }

    $(".doc").on("swipeDown" , function (e){
        if (document.body.scrollTop == 0){
            var succ = function (data){
                html = buildArticle(data);
                $(".article-container").html(html);

                $(".swipe-tip").hide();
                page = 2; //置为第二页
            }

            var fail = function (data){
                $(".swipe-tip").hide();
            }

            $(".swipe-tip").show().animate({
                "height" : $(".swipe-tip").height() - $(".swipe-tip").css("padding-top")- $(".swipe-tip").css("padding-bottom")
            } , 500 , "ease-out" , function (){
                reqData(1 , succ , fail);
            });
        }
    });

    $(window).on("scroll" , function (e){
        var isReachBottom = function() {
            return $(this).scrollTop() + $(window).height() >= $(document).height(); 
        } , locking = 0 , handler ;

        if (locking){
            return false;
        }

        if (!isReachBottom() || $(".bottom-swipe-tip").is(":visible")){
            return ;
        }

        locking = 1;

        handler = setTimeout (function (){
            clearTimeout(handler);

            var succ = function (data){
                html = buildArticle(data);
                $(html).appendTo($(".article-container"));

                $(".bottom-swipe-tip").hide();
                ++page;
                locking = 0;
            }

            var fail = function (data){
                $(".bottom-swipe-tip").hide();
                locking = 0;
            }

            $(".bottom-swipe-tip").show().animate({
                "height" : $(".swipe-tip").height() - $(".swipe-tip").css("padding-top")- $(".swipe-tip").css("padding-bottom")
            } , 300 , "ease-out" , function (){
                reqData(page , succ , fail);
            });
        } , 500);
    });    
})()