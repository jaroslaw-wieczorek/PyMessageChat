/* fade in / fade out effect between Log In / Sign Up forms  */
    var $signUp = $('.signUp');
    var $signIn = $('.signIn');
    $(".btn-member").click(function() {
      $signUp.fadeOut('slow');
      $signIn.fadeIn('slow');
    });
   $(".btn-back").click(function() {
      $signIn.fadeOut('slow');
      $signUp.fadeIn('slow');
    });