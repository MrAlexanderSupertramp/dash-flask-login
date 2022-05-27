// Basic

// < ==========  1  ========== >
var quill1 = new Quill('#editor-container1', {
  modules: {
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
      ['link', 'blockquote', 'image', 'code-block'],
      [{ list: 'ordered' }, { list: 'bullet' }]
    ]
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'  // or 'bubble'
});






function myFunction() {

  var text1 = quill1.root.innerHTML;

  var justHtml = quill1.root.innerHTML;

  var detail1 = document.getElementById('detail1');

  detail1.value = text1;

  console.log(detail1.value);
  
}

























// With Tooltip

var quill = new Quill('#quill-tooltip', {
  modules: {
    toolbar: '#toolbar-container'
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'
});

// Enable all tooltips
$('[data-toggle="tooltip"]').tooltip();

// Can control programmatically too
$('.ql-italic').mouseover();
setTimeout(function() {
  $('.ql-italic').mouseout();
}, 2500);