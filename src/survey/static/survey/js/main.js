/*global require:true, define:true, console:true, confirm:true, alert:true */
define(["jquery", "bootstrap", "select2", "jquery-cookie", "table-dnd"], function ($) {
    'use strict';

    if (!window.console) {
        console = {
            log: function () {
            }
        };
    }

// AJAX SETUP
// --------------------------------------------------------------------------------------------------------------//
    var csrftoken = $.cookie('csrftoken');
    console.log(csrftoken);

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


// STRING TEMPLATES
// --------------------------------------------------------------------------------------------------------------//
    var optionTemplate = '' +
        '<div class="checkbox">' +
        '<label for="id_{0}_{1}">' +
        '<input class="" id="id_{0}_{1}" name="{0}" checked="checked" "title="" value="{2}" type="checkbox">{3}' +
        '</label>' +
        '</div>';

    var optionUncheckedTemplate = '' +
        '<div class="checkbox">' +
        '<label for="id_{0}_{1}">' +
        '<input class="" id="id_{0}_{1}" name="{0}" title="" value="{2}" type="checkbox">{3}' +
        '</label>' +
        '</div>';


// BOOTSTRAP INIT
// --------------------------------------------------------------------------------------------------------------//
    $(window).ready(function () {

        var profileForm = $("#profile_form");
        var providerForm = $("#provider_form");
        var financialForm = $("#financial_form");
        var challengeForm = $("#challenge_form");

        var s0Review = $('#id_is_section_0_reviewed');
        var s1Review = $('#id_is_section_1_reviewed');
        var s2Review = $('#id_is_section_2_reviewed');
        var s3Review = $('#id_is_section_3_reviewed');

        profileForm.change(function () {
            $(this).data('changed', true);
        });
        challengeForm.change(function () {
            $(this).data('changed', true);
        });
        financialForm.change(function () {
            $(this).data('changed', true);
        });

        if (s0Review.prop('checked') === true) {
            profileForm.find(":input").prop("disabled", true);
            s0Review.prop("disabled", true);
        }
        if (s1Review.prop('checked') === true) {
            $("#add_provider_btn_top").toggleClass('disabled');
            $("#add_provider_btn_bottom").toggleClass('disabled');
            providerForm.find(":input").prop("disabled", true);
            s1Review.prop("disabled", true);
        }
        if (s2Review.prop('checked') === true) {
            financialForm.find(":input").prop("disabled", true);
            s2Review.prop("disabled", true);
        }
        if (s3Review.prop('checked') === true) {
            challengeForm.find(":input").prop("disabled", true);
            s3Review.prop("disabled", true);
        }

        var confirmationText = 'You have unsaved changes! \n' +
            '\tTo save your changes, click "Cancel" and then click the "Save section" button.\n' +
            '\tClick "Ok" to continue to the next section and discard changes.';

        var tabs = $('#section_tabs');
        tabs.find('a[href="#0"]').on('click', function (event) {
            event.preventDefault();
            if (challengeForm.data('changed') || financialForm.data('changed')) {
                if (confirm(confirmationText) === true) {
                    tabs.find('a[href="#0"]').tab('show');
                }
            } else {
                tabs.find('a[href="#0"]').tab('show');
            }
        });
        tabs.find('a[href="#1"]').on('click', function (event) {
            event.preventDefault();
            if (challengeForm.data('changed') || financialForm.data('changed') || profileForm.data('changed')) {
                if (confirm(confirmationText) === true) {
                    tabs.find('a[href="#1"]').tab('show');
                }
            } else {
                tabs.find('a[href="#1"]').tab('show');
            }
        });
        tabs.find('a[href="#2"]').on('click', function (event) {
            event.preventDefault();
            if (challengeForm.data('changed') || profileForm.data('changed')) {
                if (confirm(confirmationText) === true) {
                    tabs.find('a[href="#2"]').tab('show');
                }
            } else {
                tabs.find('a[href="#2"]').tab('show');
            }
        });

        tabs.find('a[href="#3"]').on('click', function (event) {
            event.preventDefault();
            if (profileForm.data('changed') || financialForm.data('changed')) {
                if (confirm(confirmationText) === true) {
                    tabs.find('a[href="#3"]').tab('show');
                }
            } else {
                tabs.find('a[href="#3"]').tab('show');
            }
        });

        var rows = $('table#provider').find("tr").length - 1;

        $('#provider-count').html(rows);


        $('#organisation-description').popover({trigger: "hover"});
        $('[data-toggle="tooltip"]').tooltip();

        $('#id_countries').select2({placeholder: "Start typing to select a country..."});
        $('#id_country_of_operation').select2({placeholder: "Start typing to select a country..."});
        $('#id_currency').select2({placeholder: "Start typing to select a currency..."});

        //$('input, textarea').placeholder();

        $('#challenge-table').tableDnD({
            onDragClass: "table-drag",
            onDrop: function (table, row) {
                var rows = table.tBodies[0].rows;
                var debugStr = "Row dropped was " + row.id + ". New order: ";
                for (var i = 0; i < rows.length; i++) {
                    debugStr += rows[i].id + " ";
                }
                //console.log(debugStr);
                var jsonForm = $.tableDnD.serialize();
                //console.log(jsonForm);

                confirmationText = "Are you sure you want to switch the rank of the challenges?";

                if (confirm(confirmationText) === true) {
                    reorderChallenges(jsonForm);
                }

                window.location.replace("/?tab=3");
            }
            //},
            //onDragStart: function (table, row) {
            //    console.log("Started dragging row " + row.id);
            //}
        });


        $('body').on('hidden.bs.modal', '.modal', function () {
            $(this).removeData('bs.modal');
        });

        $('#providerAddModal').on('loaded.bs.modal', function (event) {

            $('#id_active_countries').select2({placeholder: "Start typing to select a country..."});

            $('#other_service_provided_button').click(function (event) {
                event.preventDefault();
                var other = $('#other_service_provided')[0];
                var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
                other.value = '';
                addServiceProvided(jsonForm);
                return false;
            });

            $('#other_reliable_button').click(function (event) {
                event.preventDefault();
                var other = $('#other_reliable')[0];
                var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
                other.value = '';
                addReliable(jsonForm);
                return false;
            });

            var checkedServicesIds = $('input[name=services_provided][checked=checked]').map(function () {
                return $(this).val();
            }).get();

            var strongServiceOptionIdsAll = $('input[name=strong_services]').map(function () {
                return $(this).val();
            }).get();

            //console.log(checkedServicesIds);

            $.each(strongServiceOptionIdsAll, function (index, value) {
                if ($.inArray(value, checkedServicesIds) === -1) {
                    $('#id_strong_services').find('input[value="' + value + '"]').parent().parent().remove();
                }
            });


            $('#id_services_provided').on('click', 'input:checkbox', function (event) {
                var checked = (event.currentTarget.checked) ? true : false;
                var optionId = event.currentTarget.value;
                var optionStr = $(event.currentTarget).parent().text();

                var field = 'strong_services';
                var addedOption = String.format(optionUncheckedTemplate, field, (parseInt(optionId) - 1), optionId, optionStr);

                if (checked) {
                    $('#id_strong_services').append(addedOption);
                }
                else {
                    $('#id_strong_services').find('input[value="' + optionId + '"]').parent().parent().remove();
                }

                //console.log(addedOption);
            });
            var vasProviderForm = $("#vas_provider_form");

            vasProviderForm.on('submit', function (event) {
                event.preventDefault();
                //event.returnValue = false;
                //console.log('Interruption!!');

                var valid = true;

                if ($('#id_active_countries').select2('val').length === 0) {
                    valid = false;
                    alert('Please select at least one country');
                }

                var companyName = $("#id_vas_company_name").val();
                if (companyName.length === 0) {
                    valid = false;
                    alert('Please enter a company name');
                }

                if (valid) {
                    this.submit();
                } else {
                    $('#providerAddModal').animate({scrollTop: 0}, 600);
                }
            });

        });

        var challengesIds, challengesIdsAll;

        $("#update_biggest_challenge_1").click(function (event) {
            //event.preventDefault();
            challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
                return this.value;
            }).toArray();
            var jsonForm = $('#challenge_form').serialize();
            console.log(jsonForm);
            saveChallenges(jsonForm);

        });
        $("#update_biggest_challenge_2").click(function (event) {
            //event.preventDefault();
            challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
                return this.value;
            }).toArray();
            var jsonForm = $('#challenge_form').serialize();
            saveChallenges(jsonForm);
        });
        $("#update_biggest_challenge_3").click(function (event) {
            //event.preventDefault();
            challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
                return this.value;
            }).toArray();
            var jsonForm = $('#challenge_form').serialize();
            saveChallenges(jsonForm);
        });


        $('#challengeDetailModal').on('loaded.bs.modal', function (event) {
            //challengesIds = $('input[name=challenges][checked=checked]').map(function () {
            //    return $(this).val();
            //}).get();

            var challengeDetailForm = $("#challenge_detail_form");

            if (s3Review.prop('checked') === true) {
                challengeDetailForm.find(":input").prop("disabled", true);
            }

            var challengeSelect = $('select#id_challenge');

            challengesIdsAll = challengeSelect.find('option').map(function () {
                return $(this).val();
            }).get();

            //console.log(challengesIds);
            //console.log(challengesIdsAll);

            var colArray = $('#challenge-table').find('td:nth-child(3)').map(function () {
                return $(this).text().replace(/^\s+|\s+$/g, '');
            }).get();
            console.log(colArray);

            var url = challengeDetailForm.prop('action');
            var currentRow = url[url.length - 2] - 1;
            //console.log(currentRow);

            colArray.splice(currentRow, 1);
            //delete colArray.pop(currentRow);
            //console.log(colArray.pop(currentRow));

            //console.log(colArray);

            if (!challengeSelect.val()) {
                challengeSelect.append('<option selected="selected" value="-1">Please select an option...</option>');
            }

            $.each(challengesIdsAll, function (index, value) {
                //alert( index + ": " + value );
                if ($.inArray(value, challengesIds) === -1) {
                    challengeSelect.find('option[value="' + value + '"]').remove();
                }

                var challengeText = challengeSelect.find('option[value="' + value + '"]').text().replace(/^\s+|\s+$/g, '');

                if ($.inArray(challengeText, colArray) !== -1) {
                    challengeSelect.find('option[value="' + value + '"]').remove();
                }
            });


            $('#other_attempted_services_button').on('click', function (e) {
                e.preventDefault();

                var other = $('#other_attempted_services')[0];
                var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};

                console.log(other.value);
                other.value = '';

                addAttemptedServices(jsonForm);
                return false;
            });

            //function updateChallengeDetail(jsonForm) {
            //    var url = this.prop('action');
            //    $.ajax({
            //        url: url,
            //        type: "POST",
            //        traditional: true,
            //        data: jsonForm,
            //
            //        success: function (json) {
            //            window.location.replace("/?tab=3");
            //        },
            //        error: function (xhr) {
            //            console.log(xhr.status + ": " + xhr.responseText);
            //        }
            //    });
            //}
            //
            //$('#challenge_detail_form').on('submit', function (event) {
            //    event.preventDefault();
            //    var jsonForm = $(this).serialize();
            //    updateChallengeDetail(jsonForm);
            //    return false;
            //});

            //?? submit and review
            // below tale on left

            challengeDetailForm.on('submit', function (e) {
                //e.preventDefault();
                //e.preventDefault ? e.preventDefault() : event.returnValue = false;
                e = $.event.fix(e);
                if (e.preventDefault) {
                    e.preventDefault();
                } else {
                    e.returnValue = false;
                    console.log('Used IE8 special case!');
                }
                //event.returnValue = false;
                //console.log('Interruption!!');

                var valid = true;
                var challenge = $(this).find('#id_challenge');
                //console.log(e.val());

                if (challenge.val() === "-1") {
                    valid = false;
                    alert('Please select a challenge');
                }

                var year = parseInt($("#id_year").val());
                if (year && !(year >= 1995 && year <= 2016)) {
                    valid = false;
                    alert('Year must be between 1995 and 2016.');
                }

                var pitchSource = $("#id_pitch_source").val();
                if (pitchSource.length === 0) {
                    valid = false;
                    alert('Please indicate whether the service was pitched in-house or from an external source');
                }

                var services = $("#id_attempted_services").find("input[type=checkbox]").serialize();
                if (services.length === 0) {
                    valid = false;
                    alert('Please select at least one service');
                }

                if (valid) {
                    this.submit();
                } else {
                    $('#challengeDetailModal').animate({scrollTop: 0}, 600);
                }
            });
        });

        $(":submit").click(function () {
            $("form").data("submit-button", this.name);
        });

        profileForm.on('submit', function (event) {
            event.preventDefault();
            var button = $(this).data("submit-button");
            if (button === "close") {
                this.action = this.action + '&close=true';
                //console.log(this.action);
            }
            //console.log(button === "close");
            this.submit();
        });

        providerForm.on('submit', function (event) {
            event.preventDefault();
            var button = $(this).data("submit-button");
            if (button === "close") {
                this.action = this.action + '&close=true';
                console.log(this.action);
            }
            console.log(button === "close");
            this.submit();
        });

        financialForm.on('submit', function (event) {
            event.preventDefault();
            var button = $(this).data("submit-button");
            if (button === "close") {
                this.action = this.action + '&close=true';
                //console.log(this.action);
            }
            //console.log(button === "close");
            this.submit();
        });

        challengeForm.on('submit', function (event) {
            event.preventDefault();
            var button = $(this).data("submit-button");
            if (button === "close") {
                this.action = this.action + '&close=true';
                //console.log(this.action);
            }
            //console.log(button === "close");
            this.submit();
        });

        $('#id_revenue_streams').on('change', 'input', function (e) {
            var maxAllowed = 3;
            var cnt = $("input[name='revenue_streams']:checked").length;
            if (cnt > maxAllowed) {
                $(this).prop("checked", "");
                alert('You can select maximum ' + maxAllowed + ' revenue streams.');
            }
        });


        $('#other_challenge_button').on('click', function (e) {
            e.preventDefault();
            var other = $('#other_challenge')[0];
            var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
            //console.log(other.value);
            other.value = '';
            addChallenge(jsonForm);
            return false;
        });


        $('#other_revenue_stream_button').on('click', function (e) {
            e.preventDefault();
            var other = $('#other_revenue_stream')[0];
            var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
            //console.log(other.value);
            other.value = '';
            addRevenueStream(jsonForm);
            return false;
        });

        $('#other_roi_period_button').on('click', function (e) {
            e.preventDefault();
            var other = $('#other_roi_period')[0];

            if ($.isNumeric(other.value) && parseInt(other.value) > 0) {
                other.value = other.value + ' months';
                var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
                //console.log(other.value);
                other.value = '';
                addPeriod(jsonForm);
                return false;
            } else {
                alert('Value must be an integer to indicate the number of months');
            }
        });


        $('#progress_form').on('change', 'input[type=checkbox]', function (event) {
            //event.preventDefault();
            var count = 0;

            var jsonForm = 'csrfmiddlewaretoken=' + csrftoken + '&';

            if (s0Review.prop('checked')) {
                jsonForm += 'is_section_0_reviewed=on&';
                count++;
            }
            if (s1Review.prop('checked')) {
                jsonForm += 'is_section_1_reviewed=on&';
                count++;
            }
            if (s2Review.prop('checked')) {
                jsonForm += 'is_section_2_reviewed=on&';
                count++;
            }
            if (s3Review.prop('checked')) {
                jsonForm += 'is_section_3_reviewed=on&';
                count++;
            }

            jsonForm = jsonForm.substring(0, jsonForm.length - 1);
            console.log(jsonForm);

            var confirmString = 'Are you sure you want to mark this section as reviewed and submit it?\n' +
                'This will prevent further editing of this section. ' +
                'You will still be able to view it.';

            if (confirm(confirmString) === true) {
                reviewSection(jsonForm);
                $(this).prop("disabled", true);
            } else {
                if (event.currentTarget.checked === false) {
                    event.currentTarget.checked = true;
                } else if (event.currentTarget.checked === true) {
                    event.currentTarget.checked = false;
                }
            }

            if (count === 4) {
                $('#allDoneModal').modal();
            }
        });


        $("#provider-form").on('click', 'a[id^=delete-provider-]', function () {
            var providerPk = $(this).attr('id').split('-')[2];
            //console.log(providerPk); // sanity check
            deleteProvider(providerPk);
        });

        // Delete post on click
        $("#provider").on('click', 'a[id^=delete-provider-]', function () {
            var providerPk = $(this).attr('id').split('-')[2];
            console.log(providerPk); // sanity check
            deleteProvider(providerPk);
        });

        $('#id_revenue_stream_1').on('change', revenueStreamValidation);
        $('#id_revenue_stream_2').on('change', revenueStreamValidation);
        $('#id_revenue_stream_3').on('change', revenueStreamValidation);


        //$(document).ready(function () {
        $("#loading").fadeOut();
        //});

    });


// DEEP LINKING
// --------------------------------------------------------------------------------------------------------------//
    $(document).ready(function () {

        // queryStrip
        function queryStrip(string) {
            string = string.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
            var regex = new RegExp('[\\?&]' + string + '=([^&#]*)'),
                results = regex.exec(location.search);
            return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ''));
        }

        // Show bootstrap modal on load
        // If the modal id="terms", you can show it on page load by appending `?modal=terms` to the URL
        var modalString = queryStrip('modal'),
            modalToShow = '#' + modalString;
        if (modalString !== '') {
            $(modalToShow).modal('show');
        }

        // Show bootstrap tooltip on load
        // If the tooltip id="artistName", you can show it on page load by appending `?tooltip=artistName to the URL
        var tooltipString = queryStrip('tooltip'),
            tooltipToShow = '#' + tooltipString;
        if (tooltipString !== '') {
            $(tooltipToShow).tooltip('show');
        }

        // Show bootstrap popover on load
        // If the popover id="moreInfo", you can show it on page load by appending `?popover=moreInfo` to the URL
        var popoverString = queryStrip('popover'),
            popoverToShow = '#' + popoverString;
        if (popoverString !== '') {
            $(popoverToShow).popover('show');
        }

        // Show bootstrap tab on load
        // If the tab id="friendRequests", you can show it on page load by appending `?tab=friendRequests` to the URL
        var tabString = queryStrip('tab');
        if (tabString !== '') {
            $('.nav-tabs a[href=#' + tabString + ']').tab('show');
        }
    });


//Non prototype modifying
    if (!String.format) {
        String.format = function (format) {
            var args = Array.prototype.slice.call(arguments, 1);
            return format.replace(/{(\d+)}/g, function (match, number) {
                return typeof args[number] !== 'undefined' ? args[number] : match;
            });
        };
    }

// AJAX FORM SUBMISSION
// --------------------------------------------------------------------------------------------------------------//

    function deleteProvider(providerPk) {
        if (confirm('are you sure you want to remove this post?') === true) {
            $.ajax({
                url: "/provider/" + providerPk + "/delete/", // the endpoint
                type: "DELETE", // http method
                data: {pk: providerPk}, // data sent with the delete request
                success: function () {
                    // hide the post
                    var pc = $('#provider-count');
                    pc.html(parseInt(pc.html()) - 1);
                    $('#provider-' + providerPk).hide(); // hide the post on success
                    //console.log("Provider deletion successful");
                },

                error: function (xhr) {
                    // Show an error
                    $('#results').html("<div class='alert-box alert radius' data-alert> Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>");
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    }


    function saveChallenges(jsonForm) {
        $.ajax({
            url: "/challenge/",
            type: "POST",
            traditional: true,
            data: jsonForm,
            success: function (json) {
                var message = 'Success';
                console.log(message);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }


    function reviewSection(jsonForm) {
        $.ajax({
            url: "/review/",
            type: "POST",
            traditional: true,
            data: jsonForm,
            success: function (json) {
                var message = 'Success';
                console.log(message);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }

    function addServiceProvided(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/service/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'services_provided';
                    var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    //console.log(addedOption);
                    $("#id_" + field).append(addedOption);

                    var extraField = 'strong_services';
                    var extraAddedOption = String.format(
                        optionUncheckedTemplate, extraField, (parseInt(json.id) - 1), json.id, json.name);
                    //console.log(extraAddedOption);
                    $('#id_strong_services').append(extraAddedOption);

                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    }

    function addReliable(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/reliable/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'trust_attributes';
                    var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    console.log(addedOption);
                    $("#id_" + field).append(addedOption);
                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    }

    function addRevenueStream(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/service/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'revenue_stream';
                    var addedOption = '<option value=' + parseInt(json.id) + '>' + json.name + '</option>';
                    //var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    console.log(addedOption);
                    //$("#id_" + field).append(addedOption);
                    $("select#id_" + field + '_1').append(addedOption);
                    $("select#id_" + field + '_2').append(addedOption);
                    $("select#id_" + field + '_3').append(addedOption);
                    //$('#id_revenue_stream_1').append('<option value=46>Hello World</option>')
                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }

    }

    function addPeriod(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/period/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'acceptable_roi_wait';
                    var addedOption = '<option value=' + parseInt(json.id) + '>' + json.name + '</option>';
                    //var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    console.log(addedOption);
                    //$("#id_" + field).append(addedOption);
                    $("select#id_" + field).append(addedOption);
                    //$('#id_revenue_stream_1').append('<option value=46>Hello World</option>')
                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }

    }


    function addChallenge(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/challenge/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'challenges';
                    var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    console.log(addedOption);
                    $("#id_" + field).append(addedOption);
                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    }


    function reorderChallenges(jsonForm) {

        $.ajax({
            url: "/challenge/reorder/",
            type: "POST",
            traditional: true,
            //dataType: 'json',
            data: jsonForm,

            success: function (json) {
                console.log('Success');
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    }

    function addAttemptedServices(jsonForm) {
        if (jsonForm.name !== "") {
            $.ajax({
                url: "/service/add/",
                type: "POST",
                traditional: true,
                data: jsonForm,

                success: function (json) {
                    var field = 'attempted_services';
                    var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                    console.log(addedOption);
                    $("#id_" + field).append(addedOption);
                },
                error: function (xhr) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    }

    function unique(array) {
        return $.grep(array, function (el, index) {
            return index === $.inArray(el, array);
        });
    }

    function cleanArray(actual) {
        var newArray = [];
        for (var i = 0; i < actual.length; i++) {
            if (actual[i]) {
                newArray.push(actual[i]);
            }
        }
        return newArray;
    }

    function revenueStreamValidation(event) {
        var rs = [
            parseInt($('#id_revenue_stream_1').val()),
            parseInt($('#id_revenue_stream_2').val()),
            parseInt($('#id_revenue_stream_3').val())
        ];

        var cleanRs = cleanArray(rs);
        console.log(cleanRs);

        if (unique(rs).length !== cleanRs.length) {
            alert('Revenue streams must be unique');
            console.log(unique(rs));
            console.log($(event.currentTarget).prop('selectedIndex', 0));
        }
    }


});