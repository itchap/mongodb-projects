import { loadProducts, loadProductDetails } from './products.js';
import { sendChatMessage } from './fashionbot.js';

// Data for categories and brands
const categories = {
    'Women': {
        'Clothing': ['Dresses', 'T-shirts & tops', 'Trousers', 'Jeans', 'Shirts & Blouses', 'Jackets & Blazers', 'Sweatshirts & Hoodies', 'Skirts', 'Coats'],
        'Shoes': ['Sneakers', 'Sandals', 'Pumps', 'High heels', 'Flat shoes', 'Mules', 'Ankle boots', 'Ballerinas', 'Boots', 'Sports shoes', 'Beach shoes', 'Bridal shoes', 'House Shoes', 'Outdoor shoes'],
        'Accessories': ['Bags & cases', 'Jewellery', 'Sunglasses', 'Hats & headscarves', 'Belts', 'Watches', 'Wallets & card holders', 'Scarves', 'Blue-light glasses', 'Gloves', 'Umbrellas']
    },
    'Men': {
        'Clothing': ['T-shirts & Polos', 'Shirts', 'Sweatshirts & Hoodies', 'Trousers', 'Jeans', 'Shorts', 'Jackets', 'Suits & Tailoring', 'Coats'],
        'Shoes': ['Sneakers', 'Open shoes', 'Lace-up shoes', 'Loafers', 'Business shoes', 'Boots', 'Sports shoes', 'Outdoor shoes', 'Slippers'],
        'Accessories': ['Bags & cases', 'Jewellery', 'Sunglasses', 'Hats & headscarves', 'Belts', 'Watches', 'Wallets & card holders', 'Scarves', 'Blue-light glasses', 'Gloves', 'Umbrellas']
    }
};

const brands = {
    'Men': ['Carhartt', 'Polo Ralph Lauren', 'Armani', 'Calvin Klein', 'Diesel', 'G-Star', 'GAP', 'Helly Hansen', 'Hugo Boss', 'Lacoste', 'Levi\'s', 'Ted Baker', 'The North Face', 'Timberland', 'Tommy Hilfiger'],
    'Women': ['Anna Field', 'Levi\'s®', 'The North Face', 'Hoka', 'Rapha', 'Ciele', 'Polo Ralph Lauren', 'ARKET', 'Missoni', 'Proenza Schouler', 'The Kooples', 'MM6 Maison Margiela']
};

const designer_brands = {
    'Men': ['Dolce&Gabbana', 'Mont Blanc', 'Paul Smith', 'Prada', 'rag & bone', 'Versace', 'Vivienne Westwood'],
    'Women': ['Alexander McQueen', 'Gucci', 'Loren Stewart', 'Victoria Beckham', 'Vivienne Westwood']
};

$(document).ready(function () {
    // Initialize filters and set up event listeners for filter changes
    initializeFilters();

    // Event listener for filter form submission
    $('#filters').submit(function (event) {
        event.preventDefault(); // Prevent default form submission
        loadProducts(1); // Load products with filters applied, starting from page 1
    });

    // Event listener for sending chat messages
    $('#send-chat').click(function () {
        const question = $('#chat-input').val();
        if (question) {
            sendChatMessage(question); // Send the chat message to FashionBot
            $('#chat-input').val('');
        }
    });

    // Initial load of products
    loadProducts(1);

    // Event delegation for pagination link clicks
    $(document).on('click', '.page-link', function (e) {
        e.preventDefault();
        const page = parseInt($(this).data('page'));
        loadProducts(page); // Load products for the selected page
    });

    // Event delegation for product card clicks
    $(document).on('click', '.product-card', function () {
        const productId = $(this).data('id');
        loadProductDetails(productId); // Load details for the selected product
    });

    // Event delegation for thumbnail product clicks
    $(document).on('click', '.thumbnail-product', function () {
        const productId = $(this).data('id');
        loadProductDetails(productId); // Load details for the selected product from thumbnails
    });

    // Event listener for "Back to Products" button click
    $('#back-to-products').click(function () {
        $('#product-details').hide();
        $('#products').show();
        $('#products-title').show(); // Show the Products title
        $('#pagination').show(); // Show pagination controls
        $('#talk-to-fashionbot').hide(); // Hide FashionBot button
        window.scrollTo(0, 0); // Scroll to top
    });

    // Event listener for "Talk to FashionBot" button click
    $('#talk-to-fashionbot').click(function () {
        $('#fashionbot-chat').toggle(); // Toggle visibility of FashionBot chat
        scrollToFashionBotButton(); // Scroll so the button is at the top
    });

    // Event listener for search input changes to handle autocomplete
    $('#search').on('input', debounce(handleAutocomplete, 300));

    // Event delegation for click events on autocomplete suggestions
    $(document).on('click', '.autocomplete-suggestion', function () {
        const name = $(this).data('name');
        $('#search').val(name);
        $('#autocomplete-suggestions').hide();
        loadProducts(1); // Load products based on the selected suggestion
    });

    // Event listener to hide autocomplete suggestions when clicking outside
    $(document).click(function (event) {
        if (!$(event.target).closest('#search, #autocomplete-suggestions').length) {
            $('#autocomplete-suggestions').hide();
        }
    });
});


// Add this function to scroll so the "Talk to FashionBot" button is at the top of the screen
function scrollToFashionBotButton() {
    const fashionBotButton = $('#talk-to-fashionbot');
    $('html, body').animate({
        scrollTop: fashionBotButton.offset().top
    }, 500); // Adjust the duration as needed
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

function initializeFilters() {
    $('#gender').change(function () {
        const gender = $(this).val();
        updateCategoryAndBrandOptions(gender); // Update category and brand options based on selected gender
    });

    $('#main-category').change(function () {
        const gender = $('#gender').val();
        const mainCat = $(this).val();
        updateSubCategoryOptions(gender, mainCat); // Update sub-category options based on selected main category
    });
}

function updateCategoryAndBrandOptions(gender) {
    $('#main-category').empty().append('<option value="">All</option>');
    $('#sub-category').empty().append('<option value="">All</option>');
    $('#brand').empty().append('<option value="">All</option>');

    if (gender && categories[gender]) {
        for (const mainCat in categories[gender]) {
            $('#main-category').append(`<option value="${mainCat}">${mainCat}</option>`);
        }

        const allBrands = brands[gender].concat(designer_brands[gender]);
        allBrands.forEach(brand => {
            $('#brand').append(`<option value="${brand}">${brand}</option>`);
        });
    }
}

function updateSubCategoryOptions(gender, mainCat) {
    $('#sub-category').empty().append('<option value="">All</option>');

    if (gender && mainCat && categories[gender] && categories[gender][mainCat]) {
        categories[gender][mainCat].forEach(subCat => {
            $('#sub-category').append(`<option value="${subCat}">${subCat}</option>`);
        });
    }
}

function handleAutocomplete() {
    const query = $('#search').val();
    if (query.length > 1) {
        $.ajax({
            url: '/autocomplete',
            data: { q: query },
            success: function (data) {
                $('#autocomplete-suggestions').empty();
                data.forEach(function (item) {
                    $('#autocomplete-suggestions').append(`
                        <li class="autocomplete-suggestion" data-id="${item.id}" data-name="${item.name}">
                            ${item.name}
                        </li>
                    `);
                });
                $('#autocomplete-suggestions').show();
            },
            error: function (xhr, status, error) {
                const message = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An unexpected error occurred. Please try again later.';
                showError(message);
            }
        });
    } else {
        $('#autocomplete-suggestions').hide();
    }
}

function showError(message) {
    $('#error-message').text(message).show();
    setTimeout(function () {
        $('#error-message').hide();
    }, 5000);
}

