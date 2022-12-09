function toggleCheckboxes(source, event) {
  checkboxes = document.getElementsByClassName('fieldWrapper')[0].getElementsByTagName('input');
  for(var checkbox in checkboxes){
    checkbox.checked = source.checked;
    console.log(checkbox.checked);
  };
  console.log(checkboxes);
}

// var $checkbox = $('.select-all'),
//     undef,
//     toggleControl = function (element, state) {
//         if (!element || element === undef || state === undef) {
//             state = !$checkbox.is(':checked');
//             element = getElement($checkbox.attr('class'), state);
//         }
//         $checkbox.attr('checked', state);
//     };
// $checkbox.click(function (event) {
//     toggleControl($('label > input'), $(this).is(':checked'));
// });