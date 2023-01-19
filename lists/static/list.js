// make object of which is property of global window variable, use as namespace
window.superlists = {};
// make initialize an attribute of namespace object
window.superlists.initialize = function() {
  $('input[name="text"]').on('keypress', function(){
    $('.has-error').hide();
  });
};
