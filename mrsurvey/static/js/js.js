// FUNCTIONS

function pageLoading(loading) {
    if (loading) {
        $('.loading-container').show();
    } else {
        $('.loading-container').hide();
    }
}

function getQS(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// SINGLE PAGE MODEL

this.SurveysModel = function(config) {
    var self = this;
    var _defaultConfig = {
        itemsServiceUrl: '',
        commentsServiceUrl: '',
    };
    var _config = $.extend({}, _defaultConfig, config);


    // HANDLERS

    function loadSurveyWallet(surveyId, success, fail) {
        pageLoading(true);
        $('user-amount').hide();

        var resetPageLoading = true;

        $.ajax({
            url: _config.itemsServiceUrl,
            data: {action: 'wallet', survey_id: surveyId || getQS('survey_id')},
            method: 'GET'
        })
        .done(function(response) {
            if (response.success && response.data) {
                var wallet = response.data.wallet;
                $('.user-amount .amount').html(wallet.dollars);
                $('.user-amount').show();

                if (success) { resetPageLoading = false; }

                (success || $.noop)();
            } else {
                 if (response.message) { alert(response.message); }
                (fail || $.noop)();
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with items list!');
            (fail || $.noop)();
        })
        .always(function(response) {
            if (resetPageLoading) { pageLoading(false); }
        });
    }

    function loadSurveyItems(surveyId, success, fail) {
        pageLoading(true);

        $('.select-survey').hide();

        $.ajax({
            url: _config.itemsServiceUrl,
            data: {survey_id: surveyId || getQS('survey_id')},
            method: 'GET'
        })
        .done(function(response) {
            if (response.success && response.data) {
                var items = response.data.items,
                    template = $('#item-template').html();

                Mustache.parse(template);

                for(var i = 0; i < items.length; i++) {
                    var item = items[i],
                        $node = $(Mustache.render(template, item));

                    if (item.purchased) {
                        $node.find('.button-purchase').attr('disabled', 'disabled');
                        $node.find('.button-sell').removeAttr('disabled');
                    } else {
                        $node.find('.button-purchase').removeAttr('disabled');
                        $node.find('.button-sell').attr('disabled', 'disabled');
                    }

                    $('.items-list').append($node);
                }
                $('.items-list').show();

                (success || $.noop)();
            } else {
                if (response.message) { alert(response.message); }
                (fail || $.noop)();
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with items list!');
            (fail || $.noop)();
            pageLoading(false);
        })
        .always(function(response) {
            pageLoading(false);
        });
    }

    function loadSurvey(e) {
        $('.surveys-list li').removeClass('active');
        $('.items-list').html('');
        $element = $(e.currentTarget);
        $element.parent().addClass('active');
        document.title = "Surveys::" + $(e.currentTarget).find('.survey-name').text();

        var surveyId = $element.attr('data-survey-id');

        if (getQS('survey_id') != surveyId) {
            history.pushState({}, "Survey loading...", "?survey_id=" + surveyId);
        }
        loadSurveyWallet(surveyId, function() { loadSurveyItems(surveyId); });
    }

    function loadComments(e, success, fail) {
        var $item = $(e.currentTarget).parents('.item'),
            $body = $($(e.currentTarget).attr('href')).find('.item-comments-body'),
            itemId = $item.attr('data-item-id');


        if ($item.find('.comment').length) {
            return;
        }

        if (itemId) {
            pageLoading(true);
            $.ajax({
                url: _config.commentsServiceUrl,
                data: {item_id: itemId, survey_id: getQS('survey_id')},
                method: 'GET'
            })
            .done(function(response) {
                if (response.success && response.data) {
                    var comments = response.data.comments,
                        template = $('#comment-template').html();
                    Mustache.parse(template);

                    $body.html('');
                    for(var i = 0; i < comments.length; i++) {
                        var comment = comments[i],
                            $node = $(Mustache.render(template, comment));
                            $body.append($node);
                    }

                    (success || $.noop)();
                } else {
                    if (response.message) { alert(response.message); }
                    (fail || $.noop)();
                }
            })
            .fail(function(response) {
                alert('Something goes wrong with comments!')
                (fail || $.noop)();
            })
            .always(function(response) {
                pageLoading(false);
            });
        }
    }

    function addComment(e) {
        var $item = $(e.currentTarget).parents('.item'),
            itemId = $item.attr('data-item-id'),
            comment = $item.find('.panel-footer .comment-content').val();

        pageLoading(true);

        $.ajax({
            url: _config.commentsServiceUrl,
            data: JSON.stringify({comment: comment, item_id: itemId, survey_id: getQS('survey_id')}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var comment = response.data.comment,
                    template = $('#comment-template').html(),
                    $comments = $item.find('.item-comments-body'),
                    $node = $(Mustache.render(template, comment));

                $comments.append($node);

                $item.find('.panel-footer .comment-content').val('');
                $item.find('.comments-count').html($item.find('.item-comments-body .comment').length);
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your purchase!')
        })
        .always(function(response) {
            pageLoading(false);
        });
    }

    function purchaseItem(e) {
        var $item = $(e.currentTarget).parents('.item'),
            itemId = $item.attr('data-item-id');

        pageLoading(true);

        $.ajax({
            url: _config.itemsServiceUrl,
            data: JSON.stringify({action: 'buy', item_id: itemId, survey_id: getQS('survey_id')}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var purchase = response.data.purchase;
                $('.user-amount .amount').html(response.data.balance)

                $item.find('.button-purchase').attr('disabled', 'disabled');
                $item.find('.button-sell').removeAttr('disabled');
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your purchase!')
        })
        .always(function(response) {
            pageLoading(false);
        });
    }

    function sellItem(e) {
        var $item = $(e.currentTarget).parents('.item'),
            itemId = $item.attr('data-item-id');

        pageLoading(true);

        $.ajax({
            url: _config.itemsServiceUrl,
            data: JSON.stringify({action: 'sell', item_id: itemId, survey_id: getQS('survey_id')}),
            method: 'POST',
            contentType: 'application/json'
        })
        .done(function(response) {
            if (response.success) {
                var purchase = response.data.purchase;
                $('.user-amount .amount').html(response.data.balance)

                $item.find('.button-purchase').removeAttr('disabled');
                $item.find('.button-sell').attr('disabled', 'disabled');
            } else {
                alert(response.message);
            }
        })
        .fail(function(response) {
            alert('Something goes wrong with your selling!')
        })
        .always(function(response) {
            pageLoading(false);
        });
    }

    // HANDLERS


    function bind() {
        $('.surveys-list').on('click', 'a[data-survey-id]', loadSurvey)

        $('.items-list')
            .on('click', '.comments-header', loadComments)
            .on('click', '.add-comment', addComment)
            .on('click', '.button-purchase', purchaseItem)
            .on('click', '.button-sell', sellItem);
    }

    self.init = function() {
        bind();

        if (getQS('survey_id')) {
            loadSurvey({currentTarget: $('.surveys-list li a[data-survey-id="' + getQS('survey_id') + '"]')});
        }
    };

    self.init();
};

// COMMON INITIALIZER

$(function() {
    $('.flashes .flash').on('click', function() { $(this).fadeOut('slow'); });
});
