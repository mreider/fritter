this.HomePageModel = function(config) {
    var self = this;
    var _defaultConfig = {
        itemsServiceUrl: '',
        commentsServiceUrl: '',

        parent: '.items-list',
        purchaseSelector: '.button-purchase',
        sellSelector: '.button-sell',
        commentsCountSelector: '.comments-count',
        commentsSelector: '.comments',
        commentAddSelector: '.add-comment-send',
    };
    var _config = $.extend({}, _defaultConfig, config);

    var doNotShowWhoBought = false;


    function getAllItems() {
        $.ajax({
            url: _config.itemsServiceUrl,
            method: 'GET'
        })
        .done(function(respose) {
            if (respose.success && respose.data) {
                var items = respose.data.items,
                    template = $('#item-template').html();

                Mustache.parse(template);

                for(var i = 0; i < items.length; i++) {
                    var item = items[i],
                        $node = $(Mustache.render(template, item));

                    if (item.purchased) {
                        $node.find(_config.purchaseSelector).attr('disabled', 'disabled');
                        $node.find(_config.sellSelector).removeAttr('disabled');
                    } else {
                        $node.find(_config.purchaseSelector).removeAttr('disabled');
                        $node.find(_config.sellSelector).attr('disabled', 'disabled');
                    }

                    $(_config.parent).append($node);
                }
            }
        })
        .fail(function(respose) {
            alert('Something goes wrong with items list!')
        })
        .always(function(respose) {
        });
    }

    function loadComments(e) {
        var $head = $(e.currentTarget),
            $body = $head.next('.collapse-body');
        var itemId = $head.parents('.item').attr('data-item-id');

        if (itemId) {
            $.ajax({
                url: _config.commentsServiceUrl,
                data: {item_id: itemId},
                method: 'GET'
            })
            .done(function(response) {
                $body.removeClass('loading');

                if (response.success && response.data) {

                    var comments = response.data.comments,
                        template = $('#comment-template').html();
                    Mustache.parse(template);

                    for(var i = 0; i < comments.length; i++) {
                        var comment = comments[i],
                            $node = $(Mustache.render(template, comment));
                            $body.append($node);
                    }
                }

                $body.append($('#add-comment-template').html());
            })
            .fail(function(response) {
                alert('Something goes wrong with comments!')
            })
            .always(function(response) {
            });
        }
    }

    function addComment(e) {
        var $item = $(e.currentTarget).parents('.item'),
            itemId = $item.attr('data-item-id'),
            comment = $item.find('.add-comment-content').val();

        $.ajax({
            url: _config.commentsServiceUrl,
            data: JSON.stringify({comment: comment, item_id: itemId}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var comment = response.data.comment,
                    template = $('#comment-template').html(),
                    $lastComment = $item.find('.comments .comment').last(),
                    $node = $(Mustache.render(template, comment));

                $lastComment.after($node);
                $item.find('.add-comment-content').val('');
                $item.find('.comments-count').html($item.find('.comments .comment').length);
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your purchase!')
        })
        .always(function(response) {
        });
    }

    function showWhoBoughtSame(itemId, name, users) {
        if (users.length) {
            var template = $('#who-bought').html();
            Mustache.parse(template);
            $node = $(Mustache.render(template, {'name': name, 'users': users}));

            $('.notification .content').html('').append($node);

            $('.notification').fadeIn();
        }
    }

    function purchaseItem(e) {
        var itemId = $(e.currentTarget).parents('.item').attr('data-item-id');
        $.ajax({
            url: _config.itemsServiceUrl,
            data: JSON.stringify({action: 'buy', item_id: itemId}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var purchase = response.data.purchase,
                    $item = $(e.currentTarget).parents('.item');
                $('.user-money .amount').html(purchase.user.dollars)

                $item.find(_config.purchaseSelector).attr('disabled', 'disabled');
                $item.find(_config.sellSelector).removeAttr('disabled');

                showWhoBoughtSame(itemId, purchase.item.name, response.data.who_bought);
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your purchase!')
        })
        .always(function(response) {
        });
    }

    function sellItem(e) {
        var itemId = $(e.currentTarget).parents('.item').attr('data-item-id');
        $.ajax({
            url: _config.itemsServiceUrl,
            data: JSON.stringify({action: 'sell', item_id: itemId}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var purchase = response.data.purchase,
                    $item = $(e.currentTarget).parents('.item');
                $('.user-money .amount').html(purchase.user.dollars)

                $item.find(_config.purchaseSelector).removeAttr('disabled');
                $item.find(_config.sellSelector).attr('disabled', 'disabled');
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your selling!')
        })
        .always(function(response) {
        });
    }

    function bind() {
        getAllItems();

        var $parent = $(_config.parent);
        $parent
        .on('click', '.collapse .collapse-head', function(e) {
            $(this).parent().find('.collapse-body').toggleClass('expanded').slideToggle('fast');
            $(this).parent().toggleClass('active');
            e.preventDefault();
        })
        .on('click', _config.purchaseSelector + ':not([disabled])', purchaseItem)
        .on('click', _config.sellSelector + ':not([disabled])', sellItem)
        .on('click', '.comments-head', function(e) {
            $body = $(this).next();
            $body.html('').addClass('loading');

            loadComments(e);
        })
        .on('click', _config.commentAddSelector, addComment)

        $('.notification .close').on('click', function() {
            $('.notification').fadeOut();
        });
    }

    bind();
};