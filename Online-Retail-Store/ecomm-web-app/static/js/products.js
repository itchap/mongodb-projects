export function loadProducts(page) {
    let search = $('#search').val();
    let mainCategory = $('#main-category').val();
    let subCategory = $('#sub-category').val();
    let gender = $('#gender').val();
    let brand = $('#brand').val();

    showLoadingSpinner(true); // Show loading spinner

    $.ajax({
        url: '/products',
        data: {
            q: search,
            category: mainCategory,
            sub_category: subCategory,
            gender: gender,
            brand: brand,
            page: page
        },
        success: function (data) {
            renderProducts(data.products); // Render the products
            setupPagination(data.current_page, data.total_pages); // Setup pagination
            showLoadingSpinner(false); // Hide loading spinner
            window.scrollTo(0, 0); // Scroll to top
        },
        error: function (xhr, status, error) {
            showLoadingSpinner(false); // Hide loading spinner
            const message = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An unexpected error occurred. Please try again later.';
            showError(message);
        }
    });
}

function renderProducts(products) {
    $('#products').empty();
    $('#product-details').hide();
    $('#products').show();
    if (products.length === 0) {
        $('#products').append('<p>No products found.</p>');
    } else {
        products.forEach(function (product) {
            $('#products').append(`
                <div class="col-md-4">
                    <div class="card mb-4 shadow-sm product-card" data-id="${product._id}">
                        <img src="${product.images[0]}" class="card-img-top" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">${product.description}</p>
                            <p class="card-text"><strong>€${product.price}</strong></p>
                            <p class="card-text">Score: ${product.score ? product.score.toFixed(2) : 'N/A'}</p>
                            <p class="card-text">Sponsored: ${product.sponsored ? 'Yes' : 'No'}</p>
                        </div>
                    </div>
                </div>
            `);
        });
    }
}

function setupPagination(currentPage, totalPages) {
    $('#pagination').empty();

    const maxPagesToShow = 5; // Maximum number of page links to show at a time
    let startPage, endPage;

    if (totalPages <= maxPagesToShow) {
        // If total pages are less than maxPagesToShow, show all pages
        startPage = 1;
        endPage = totalPages;
    } else {
        // Calculate the start and end pages
        const maxPagesBeforeCurrentPage = Math.floor(maxPagesToShow / 2);
        const maxPagesAfterCurrentPage = Math.ceil(maxPagesToShow / 2) - 1;

        if (currentPage <= maxPagesBeforeCurrentPage) {
            // If current page is near the start
            startPage = 1;
            endPage = maxPagesToShow;
        } else if (currentPage + maxPagesAfterCurrentPage >= totalPages) {
            // If current page is near the end
            startPage = totalPages - maxPagesToShow + 1;
            endPage = totalPages;
        } else {
            // If current page is somewhere in the middle
            startPage = currentPage - maxPagesBeforeCurrentPage;
            endPage = currentPage + maxPagesAfterCurrentPage;
        }
    }

    // Add First and Previous buttons
    if (currentPage > 1) {
        $('#pagination').append(`
            <li class="page-item">
                <a class="page-link" href="#" data-page="1">First</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
            </li>
        `);
    }

    // Add page number links
    for (let page = startPage; page <= endPage; page++) {
        $('#pagination').append(`
            <li class="page-item ${page === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" data-page="${page}">${page}</a>
            </li>
        `);
    }

    // Add Next and Last buttons
    if (currentPage < totalPages) {
        $('#pagination').append(`
            <li class="page-item">
                <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="#" data-page="${totalPages}">Last</a>
            </li>
        `);
    }
}

export function loadProductDetails(productId) {
    showLoadingSpinner(true); // Show loading spinner

    $.ajax({
        url: `/products/${productId}`,
        success: function (data) {
            $('#products').hide();
            $('#products-title').hide(); // Hide the Products title
            $('#pagination').hide(); // Hide pagination controls
            $('#product-details').data('product-id', data._id);
            $('#product-details-content').empty().append(`
                <img src="${data.images[0]}" class="img-fluid" alt="${data.name}">
                <h5>${data.name}</h5>
                <p><strong>Price:</strong> €${data.price}</p>
                <p><strong>Description:</strong> ${data.description}</p>
                <p><strong>Brand:</strong> ${data.brand}</p>
                <p><strong>Category:</strong> ${data.main_category} > ${data.sub_category}</p>
                <p><strong>Sizes:</strong> ${data.sizes.join(', ')}</p>
                <p><strong>Colors:</strong> ${data.colors.join(', ')}</p>
                <p><strong>Material:</strong> ${data.material}</p>
                <p><strong>Stock:</strong> ${data.stock}</p>
                <p><strong>Availability:</strong> ${data.availability}</p>
                <p><strong>Rating:</strong> ${data.rating}</p>
                <p><strong>Reviews:</strong></p>
                <ul>
                    ${data.reviews.map(review => `<li>${review.author}: ${review.comment} (${review.rating} stars)</li>`).join('')}
                </ul>
                <p><strong>Created At:</strong> ${new Date(data.created_at).toLocaleString()}</p>
                <p><strong>Updated At:</strong> ${new Date(data.updated_at).toLocaleString()}</p>
                <p><strong>On Sale:</strong> ${data.on_sale}</p>
                <p><strong>Pre-Owned:</strong> ${data.pre_owned}</p>
                <p><strong>Condition:</strong> ${data.condition}</p>
                <p><strong>Sponsored:</strong> ${data.sponsored}</p>
                <p><strong>New In:</strong> ${data.new_in}</p>
            `);
            $('#product-details').show();
            $('#talk-to-fashionbot').show();  // Show the FashionBot button here
            loadRecommendations(productId);
            showLoadingSpinner(false); // Hide loading spinner
            window.scrollTo(0, 0); // Scroll to top
        },
        error: function (xhr, status, error) {
            showLoadingSpinner(false); // Hide loading spinner
            const message = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An unexpected error occurred. Please try again later.';
            showError(message);
        }
    });
}

function loadRecommendations(productId) {
    $.ajax({
        url: `/products/${productId}/recommendations`,
        success: function (data) {
            $('#recommendations-thumbnails').empty();
            if (data.length === 0) {
                $('#recommendations-thumbnails').append('<p>No recommendations found.</p>');
            } else {
                data.slice(0, 3).forEach((item) => {
                    $('#recommendations-thumbnails').append(`
                        <img src="${item.images[0]}" class="thumbnail-product" alt="${item.name}" data-id="${item._id}">
                    `);
                });
            }
        },
        error: function (xhr, status, error) {
            const message = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An unexpected error occurred. Please try again later.';
            showError(message);
        }
    });
}

function showLoadingSpinner(show) {
    if (show) {
        $('#loading-spinner').show();
    } else {
        $('#loading-spinner').hide();
    }
}

function showError(message) {
    $('#error-message').text(message).show();
    setTimeout(function () {
        $('#error-message').hide();
    }, 5000);
}