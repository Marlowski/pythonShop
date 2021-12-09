$(function() {
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
});