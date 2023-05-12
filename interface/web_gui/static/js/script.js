$(document).ready(function() {
    $('.element').first().find('.attribute-input').attr('readonly', false);

    // Category filter buttons event
    $('.category-filter-button').on('click', handleCategoryFilterClick);

    // Toggle between grid and list view
    $('#toggle-view-btn').on('click', toggleView);

    // Checkbox and filter events
    $('.done-checkbox').on('change', handleCheckboxChange);
    $('#filter-completed').on('change', filterCompleted);
    $('#tagComboBox').on('change', searchAndUpdateElements);
    $('#searchBar').on('input', searchAndUpdateElements);

    // Remove button event
    $('.remove-button').on('click', handleRemoveClick);

    $('.attribute-input').keypress(function(event) {
        if (event.keyCode == 13) {  // 13 is the key code for ENTER
            event.preventDefault();
            createNewElement();
        }
    });
});

let selectedCategory = null;
function handleCategoryFilterClick() {
    selectedCategory = $(this).data('category');

    // Show all elements
    $('.element:not(:first)').show();

    // If a specific category is selected, hide elements that do not belong to this category
    if (selectedCategory) {
        $('.element:not(:first)').each(function () {
            const elementCategory = $(this).find('.done-checkbox').data('element-category');
            if (elementCategory !== selectedCategory) {
                $(this).hide();
            }
        });
    }

    // Update the counter label
    updateCounterLabel();

    // If a new element is being created, set the category field to the selected category and make it read-only
    const categoryInput = $('#first-category-input');
    if (selectedCategory) {
        categoryInput.val(selectedCategory).prop('readonly', true).css("background-color", "grey");
    } else {
        categoryInput.val('').prop('readonly', false).css("background-color", "");
    }
}

function filterCompleted() {
    const filterCheckbox = $('#filter-completed').is(':checked');
    $('.element:not(:first)').each(function () {
        const doneCheckbox = $(this).find('.done-checkbox');
        const elementCategory = doneCheckbox.data('element-category');
        const isElementCompleted = doneCheckbox.is(':checked');

        if (filterCheckbox && isElementCompleted) {
            $(this).hide();
        } else if (!selectedCategory || elementCategory === selectedCategory) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });

    updateCounterLabel();
}

function toggleView() {
    const centralWidget = $('#centralWidget .grid-container, #centralWidget .list-container');
    centralWidget.toggleClass('grid-container list-container');
}

function handleCheckboxChange() {
    const elementTitle = $(this).data('element-title');
    const elementCategory = $(this).data('element-category');
    const isChecked = $(this).is(':checked');

    // Update the 'done' status of the Element object
    $.ajax({
        url: '/update_done',
        method: 'POST',
        data: {
            'element_title': elementTitle,
            'element_category': elementCategory,
            'is_done': isChecked
        },
        success: function(response) {
            if (response.success) {
                updateCounterLabel();
                filterCompleted();
            }
        }
    });
}

function searchAndUpdateElements() {
    const searchTerm = $('#searchBar').val().toLowerCase();
    const searchTag = $('#tagComboBox').val();
    const minSearchLength = 2;

    if (searchTerm.length < minSearchLength) {
        $('.element').show();
        removeHighlight();
        updateCounterLabel();
        return;
    }

    $('.element').each(function () {
        const element = $(this);
        const attributeDiv = element.find('.attribute-' + searchTag);
        let attributeValue = attributeDiv.text();

        if (!attributeDiv.has('input').length) {
            attributeValue = attributeValue.toLowerCase();
        }

        if (attributeValue.includes(searchTerm)) {
            element.show();
            const highlightedText = highlight(attributeDiv.text(), searchTerm);
            attributeDiv.html(highlightedText);
        } else {
            element.hide();
        }
    });

    updateCounterLabel();
}

function highlight(text, searchTerm) {
    const index = text.toLowerCase().indexOf(searchTerm.toLowerCase());
    if (index === -1) {
        return text;
    }

    return text.slice(0, index) + '<mark>' + text.slice(index, index + searchTerm.length) + '</mark>' + text.slice(index + searchTerm.length);
}

function removeHighlight() {
    $('.attribute:not(:has(input))').each(function () { $(this).text($(this).text()); });
}

function createNewElement() {
    // Gather the attribute values from the editable element
    let attributes = {};
    $('.element').first().find('input[type="text"]').each(function() {
        let attributeName = $(this).data('attribute-name');
        let attributeValue = $(this).val();
        attributes[attributeName] = attributeValue;
    });

    // Send the attribute values to the server
    $.ajax({
        url: '/create_element',
        method: 'POST',
        data: attributes,
        success: function(response) {
            if (response.success) {
                // If the server successfully created the new element, refresh the page to show it
                location.reload();
            } else {
                alert('Failed to create new element: ' + response.error);
            }
        }
    });
}

function handleRemoveClick() {
    const elementTitle = $(this).data('element-title');
    const elementCategory = $(this).data('element-category');

    // Confirm the removal
    if (confirm(`Remove ${elementTitle}?`)) {
        // Send a request to the server to remove the element
        $.ajax({
            url: '/remove_element',
            method: 'POST',
            data: {
                'element_title': elementTitle,
                'element_category': elementCategory
            },
            success: function(response) {
                if (response.success) {
                    // If the server successfully removed the element, refresh the page to reflect the changes
                    location.reload();
                } else {
                    alert('Failed to remove element: ' + response.error);
                }
            }
        });
    }
}

function updateCounterLabel() {
    let visibleElements = $('.element:visible').length - 1;
    $('#counterLabel').text(`Displaying ${visibleElements} elements`);
}
