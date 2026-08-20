function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const [key, ...valueParts] = cookie.trim().split('=');

        if (key === name) {
            return decodeURIComponent(valueParts.join('='));
        }
    }

    return null;
}


function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // Review page authentication.
    if (!token && document.getElementById('review-form')) {
        window.location.href = 'index.html';
        return null;
    }

    
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    return token;
}


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


async function fetchPlace(placeId) {
    const response = await fetch(`/api/v1/places/${placeId}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch place: ${response.status}`);
    }

    return await response.json();
}


async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch('/api/v1/reviews/', {
        method: 'POST',

        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },

        body: JSON.stringify({
            place_id: placeId,
            text: reviewText,
            rating: Number(rating)
        })
    });

    if (!response.ok) {
        let message = 'Failed to submit review.';

        try {
            const data = await response.json();

            if (data.error) {
                message = data.error;
            } else if (data.message) {
                message = data.message;
            }
        } catch (error) {
            
        }

        throw new Error(message);
    }

    return await response.json();
}


function showReviewMessage(message, type) {
    const messageElement =
        document.getElementById('review-message');

    if (!messageElement) {
        alert(message);
        return;
    }

    messageElement.textContent = message;
    messageElement.className = `review-message ${type}`;
    messageElement.style.display = 'block';
}


async function setupReviewPage() {
    const reviewForm = document.getElementById('review-form');

    if (!reviewForm) {
        return;
    }

    const token = checkAuthentication();

    if (!token) {
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        showReviewMessage(
            'Invalid place ID.',
            'error'
        );
        return;
    }

    // Get the place information.
    try {
        const place = await fetchPlace(placeId);

        const subtitle =
            document.getElementById('review-subtitle');

        if (subtitle) {
            subtitle.textContent =
                `Share your experience at ${place.title}`;
        }

    } catch (error) {
        console.error(
            'Error loading place:',
            error
        );

        showReviewMessage(
            'Unable to load the place information.',
            'error'
        );

        return;
    }


    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText =
            document.getElementById('review')
                .value
                .trim();

        const rating =
            document.getElementById('rating').value;


        if (!rating) {
            showReviewMessage(
                'Please select a rating.',
                'error'
            );
            return;
        }


        if (!reviewText) {
            showReviewMessage(
                'Please enter a review.',
                'error'
            );
            return;
        }


        const submitButton =
            reviewForm.querySelector(
                'button[type="submit"]'
            );


        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
        }


        try {
            await submitReview(
                token,
                placeId,
                reviewText,
                rating
            );


            showReviewMessage(
                'Review submitted successfully!',
                'success'
            );


            reviewForm.reset();

        } catch (error) {
            console.error(
                'Error submitting review:',
                error
            );

            showReviewMessage(
                error.message ||
                'Failed to submit review.',
                'error'
            );

        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit review';
            }
        }
    });
}


async function fetchPlaces() {
    try {
        const response =
            await fetch('/api/v1/places/');

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status}`
            );
        }

        const places = await response.json();

        displayPlaces(places);

    } catch (error) {
        console.error(
            'Error fetching places:',
            error
        );
    }
}


function displayPlaces(places) {
    const placesList =
        document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';


    places.forEach((place) => {
        const placeElement =
            document.createElement('div');

        placeElement.className = 'place-card';
        placeElement.dataset.price = place.price;

        placeElement.innerHTML = `
            <h2>${place.title}</h2>

            <p>${place.description || ''}</p>

            <p class="price">
                $${place.price} / night
            </p>

            <a
                href="place.html?id=${place.id}"
                class="details-button"
            >
                View Details
            </a>
        `;

        placesList.appendChild(placeElement);
    });
}


function filterPlaces() {
    const priceFilter =
        document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const selectedPrice =
        priceFilter.value;

    const placeCards =
        document.querySelectorAll('.place-card');


    placeCards.forEach((placeCard) => {
        const placePrice =
            parseFloat(placeCard.dataset.price);


        if (selectedPrice === 'all') {
            placeCard.style.display = 'block';
            return;
        }


        const maxPrice =
            parseFloat(selectedPrice);

        if (placePrice <= maxPrice) {
            placeCard.style.display = 'block';
        } else {
            placeCard.style.display = 'none';
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {

    // Review page
    setupReviewPage();


    // Index page
    const priceFilter =
        document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener(
            'change',
            filterPlaces
        );

        fetchPlaces();
    } else {
        checkAuthentication();
    }
});
