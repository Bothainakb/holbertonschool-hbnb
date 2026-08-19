let token = null;

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split('=');

        if (key === name) {
            return value;
        }
    }

    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function checkAuthentication() {
    token = getCookie('token');

    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        addReviewSection.style.display = 'none';

        if (loginLink) {
            loginLink.style.display = 'block';
        }
    } else {
        addReviewSection.style.display = 'block';

        if (loginLink) {
            loginLink.style.display = 'none';
        }
    }
}

async function fetchPlaceDetails(placeId) {
    try {
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(
            `/api/v1/places/${placeId}`,
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const place = await response.json();

        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error fetching place details:', error);

        const placeDetails = document.getElementById('place-details');

        placeDetails.innerHTML = `
            <p>Unable to load place details.</p>
        `;
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    placeDetails.innerHTML = '';

    const title = document.createElement('h1');
    title.textContent = place.title || 'Unnamed Place';

    const description = document.createElement('p');
    description.textContent = place.description || 'No description available.';

    const price = document.createElement('p');
    price.className = 'price';
    price.textContent = `$${place.price} / night`;

    const location = document.createElement('p');
    location.textContent =
        `Location: ${place.latitude}, ${place.longitude}`;

    placeDetails.appendChild(title);
    placeDetails.appendChild(description);
    placeDetails.appendChild(price);
    placeDetails.appendChild(location);

    if (place.amenities && place.amenities.length > 0) {
        const amenitiesTitle = document.createElement('h2');
        amenitiesTitle.textContent = 'Amenities';

        const amenitiesList = document.createElement('ul');

        place.amenities.forEach((amenity) => {
            const item = document.createElement('li');

            if (typeof amenity === 'string') {
                item.textContent = amenity;
            } else {
                item.textContent =
                    amenity.name || 'Unnamed amenity';
            }

            amenitiesList.appendChild(item);
        });

        placeDetails.appendChild(amenitiesTitle);
        placeDetails.appendChild(amenitiesList);
    }

    if (place.reviews && place.reviews.length > 0) {
        const reviewsTitle = document.createElement('h2');
        reviewsTitle.textContent = 'Reviews';

        const reviewsList = document.createElement('div');

        place.reviews.forEach((review) => {
            const reviewElement = document.createElement('div');
            reviewElement.className = 'review';

            const reviewText = document.createElement('p');
            reviewText.textContent =
                review.text || 'No review text.';

            const rating = document.createElement('p');
            rating.textContent =
                `Rating: ${review.rating || 'N/A'}/5`;

            reviewElement.appendChild(reviewText);
            reviewElement.appendChild(rating);

            reviewsList.appendChild(reviewElement);
        });

        placeDetails.appendChild(reviewsTitle);
        placeDetails.appendChild(reviewsList);
    } else {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'No reviews yet.';
        placeDetails.appendChild(noReviews);
    }
}

const placeId = getPlaceIdFromURL();

if (!placeId) {
    document.getElementById('place-details').innerHTML = `
        <p>No place ID was provided.</p>
    `;
} else {
    checkAuthentication();
    fetchPlaceDetails(placeId);
}
