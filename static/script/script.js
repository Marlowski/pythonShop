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
   $('#search-select').on('change', function () {
      let placeholderText;
      switch($('#search-select').val()) {
         case "default":
            placeholderText = "Suche";
            break;
         case "desc":
            placeholderText = "Suche (Beschreibung)";
            break;
         case "rating":
            placeholderText = "Suche (Bewertungen)";
            break;
         default:
            placeholderText = "Suche";
      }
      $('#searchbar').attr("placeholder", placeholderText);
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

   //click starr rating (user selected start amount)
   $('.star-elem').on('click', function () {
      //show send button
      $('.product-rating-submit-wrapper button').css('display', 'block');

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

   //send star rating handler
   $('.product-rating-submit-wrapper button').on('click', function () {
      let data = {
         'rating': $('.product-rating-wrapper').attr('data-rating-value')
      }
      djangoPostRequest(window.location.pathname, data);
   });

   //set total stars on load
   let rating = parseInt($('.total-product-rating-container').attr('data-average-rating'));
   for(let i=0; i < rating; i++) {
      let className = ".total-" + i;
      $(className).addClass('selected');
   }

   // Cart ajax handler
   //done in javascript to keep scroll position after refresh and therefor make it easy to add, remove etc. items from cart
   $('.cq_add_btn').on('click', function () {
      let data = {
         'change_quantity_add': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data)
   });

   $('.cq_rem_btn').on('click', function () {
      let data = {
         'change_quantity_rem': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data)
   });

   $('.remove_item_btn').on('click', function () {
      let data = {
         'remove_item': $(this).attr('value')
      }
      djangoPostRequest(window.location.pathname, data)
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