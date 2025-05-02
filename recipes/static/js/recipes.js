/* jshint esversion: 11 */
/* global $ */

$(document).ready(function () {
    const emptyFormHtml = $('.ingredient-form').first().clone()[0].outerHTML;
  
    function initializeSelect2() {
      $('.select2-ingredient').select2({
        theme: 'bootstrap-5',
        placeholder: 'Search for an ingredient...',
        width: '100%',
        ajax: {
            url: document.getElementById('ingredient-search-url').dataset.url,
          dataType: 'json',
          delay: 250,
          data: function (params) {
            return { q: params.term };
          },
          processResults: function (data) {
            return { results: data.results || [] };
          },
          cache: true
        },
        minimumInputLength: 1
      });
    }
  
    initializeSelect2();
  
    $('#add-ingredient').click(function () {
      const formCount = parseInt($('#id_recipe_ingredients-TOTAL_FORMS').val());
      const newFormHtml = emptyFormHtml.replace(/-\d+-/g, `-${formCount}-`);
      const $newForm = $(newFormHtml);
  
      $('#ingredient-forms').append($newForm);
      $newForm.find('input[type="text"]').val('');
      $newForm.find('select').val(null).trigger('change');
  
      $newForm.find('.select2-ingredient').select2({
        theme: 'bootstrap-5',
        placeholder: 'Search for an ingredient...',
        width: '100%',
        ajax: {
          url: '/api/ingredients/',
          dataType: 'json',
          delay: 250,
          data: function (params) {
            return { q: params.term };
          },
          processResults: function (data) {
            return { results: data.results || [] };
          },
          cache: true
        },
        minimumInputLength: 1
      });
  
      $('#id_recipe_ingredients-TOTAL_FORMS').val(formCount + 1);
    });
  
    $(document).on('click', '.remove-form', function () {
      const $form = $(this).closest('.ingredient-form');
      const formCount = $('.ingredient-form').length;
  
      if (formCount > 1) {
        $form.find('.select2-ingredient').select2('destroy');
        $form.remove();
  
        $('.ingredient-form').each(function (index) {
          $(this).find(':input').each(function () {
            const $input = $(this);
            const name = $input.attr('name')?.replace(/-\d+-/, `-${index}-`);
            const id = $input.attr('id')?.replace(/-\d+-/, `-${index}-`);
            if (name) $input.attr('name', name);
            if (id) $input.attr('id', id);
          });
        });
  
        $('#id_recipe_ingredients-TOTAL_FORMS').val(formCount - 1);
      } else {
        $form.find('input[type="text"]').val('');
        $form.find('select').val(null).trigger('change');
      }
    });
  });
  