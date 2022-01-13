$(function() {
   //cookie script
   //if no back button exists, cookie current url
   if(!$('.back-btn').length) {
      $.cookie("prev-url", window.location.href, {path:"/", SameSite:"Lax"});
   } else {
      //back btn exists set href to cookied url or home if prev-url = undefined or if cookie points to current url
      if($.cookie("prev-url") && $.cookie("prev-url") !== window.location.href) {
         $('.back-btn').attr("href", $.cookie("prev-url"));
      } else {
         $('.back-btn').attr("href", "http://127.0.0.1:8000");
      }
   }

   //search select manager
   //assure that after refresh stored elem is selected
   if ($('#search-select').length) {
      $('#search-select').val(localStorage.getItem("search-type"));
      setSearchSelection();
   }

   $('#search-select').on('change', function () {
      //save selected for refresh
      localStorage.setItem("search-type", $(this).val());
      setSearchSelection();
   });

   //product page star rating handler
   $('.star-elem').hover(
     function () {
        //mouseenter
        //get class identifier number
        let currentElem = parseInt($(this).attr('class').split(/\s+/)[1].split("-")[1]);
        for (let i=currentElem; i > 0; i--) {
           let className = ".star-" + i;
           $(className).find('svg').css("fill","#fba200");
        }
     }, function () {
         //mouseleave
          $('.star-elem').find('svg').css("fill","none");
     }
   );

   //click star rating (user selected start amount)
   $('.star-elem').on('click', function () {
      //show send button
      $('.product-rating-submit-wrapper').slideDown();

      //make sure everything is unselected before setting new select amount
      $('.star-elem').removeClass('selected');

      let currentElem = parseInt($(this).attr('class').split(/\s+/)[1].split("-")[1]);
      //save selected value
      $('.product-rating-wrapper').attr('data-rating-value', currentElem);

      for (let i=currentElem; i > 0; i--) {
         let className = ".star-" + i;
         $(className).addClass('selected');
      }
   });

   //handle star rating submit -> send data to python server
   $('.product-rating-submit-wrapper').on('submit', function (e) {
      e.preventDefault();
      let data = {
         'rating': $('.product-rating-wrapper').attr('data-rating-value'),
         'comment': $('#product-rating-comment').val()
      }
      djangoPostRequest(window.location.pathname, data);
   });

   //set total stars on load
   $('.total-product-rating-container').each(function () {
      let rating = parseInt($(this).attr('data-average-rating'));

      for(let i=1; i <= rating; i++) {
         let className = ".total-" + i;
         $(this).find(className).addClass('selected');
      }
   });

   //rating comments delete & edit handler
   $('#action-delete').on('click', function () {
      let data = {
         'action': "delete",
         'rating_id': $(this).closest("li").attr('data-rating-id')
      }
      djangoPostRequest(window.location.pathname, data);
   });

   $('#action-edit').on('click', function () {
      //togglewise handle edit btn
      if($('#action-edit').attr('data-active-edit') === "true") {
         document.location.reload();
         return
      }

      //create textarea
      let input = document.createElement("textarea");
      input.classList.add("edit-rating-textarea");

      //replace textnode with textarea
      let commentElem = $(this).closest("li").find('.rating_comment');
      input.value = commentElem.text();
      commentElem.replaceWith(input);

      //show save btn
      $('#action-edit-save').fadeIn();
      $('#action-edit').attr('data-active-edit', true).css("background-color", "#ad1010");
   });

   $('#action-edit-save').on('click', function () {
      let newText = $(this).closest("li").find(".edit-rating-textarea")[0].value
      let data = {
         "action": "edit",
         'rating_id': $(this).closest("li").attr('data-rating-id'),
         "comment": newText
      }
      djangoPostRequest(window.location.pathname, data)
   });

   //evaluate comment (helpful, not helpful, report) handler
   $('.evaluate_btn').on('click', function () {
      let evValue = null
      switch ($(this).attr("id")) {
         case "evaluate-helpful":
            evValue = "POS";
            break;
         case "evaluate-not-helpful":
            evValue = "NEG";
            break;
         case "evaluate-report":
            evValue = "REP";
            break;
         default:
            console.error("Evaluation switch cant find matching parameter");
            return;
      }
      let data = {
         "action": "evaluate",
         "evaluation": evValue,
         "rating_id": $(this).closest("li").attr('data-rating-id')
      }
      djangoPostRequest(window.location.pathname, data);
   });

   // Cart ajax handler
   //done in javascript to keep scroll position after refresh and therefor make it easy to add, remove etc. items from cart
   $('.cq_add_btn').on('click', function () {
      let data = {
         'change_quantity_add': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data);
   });

   $('.cq_rem_btn').on('click', function () {
      let data = {
         'change_quantity_rem': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data);
   });

   $('.remove_item_btn').on('click', function () {
      let data = {
         'remove_item': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data);
   });
});

function djangoPostRequest(url, data) {
   $.ajax({
      method: 'POST',
      headers: {
         'X-CSRFToken': $.cookie('csrftoken'),
      },
      mode: 'same-origin',
      url: url,
      data: data,
      success: function () {
         document.location.reload();
      }
   });
}

function setSearchSelection() {
         let placeholderText;
      switch($('#search-select').val()) {
         case "default":
            placeholderText = "Suche";
            $('.sip-star').removeClass('shown');
            $('.sip-size').removeClass('shown');
            break;
         case "size":
            placeholderText = "Suche (Ringbreite)";
            $('.sip-star').removeClass('shown');
            $('.sip-size').addClass('shown');
            break;
         case "rating":
            placeholderText = "Suche (Rating (3, 2-5))";
            $('.sip-star').addClass('shown');
            $('.sip-size').removeClass('shown');
            break;
         default:
            placeholderText = "Suche";
            $('.sip-star').removeClass('shown');
            $('.sip-size').removeClass('shown');
      }
      $('#searchbar').attr("placeholder", placeholderText);
}