$(document).ready(function () {
  $("#record_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".table .record").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});
