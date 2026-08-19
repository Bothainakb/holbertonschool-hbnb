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

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
}

async function fetchPlaces() {
    try {
        const response = await fetch('/api/v1/places/');

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const places = await response.json();

        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeElement = document.createElement('div');

        placeElement.className = 'place-card';

        placeElement.innerHTML = `
            <h2>${place.title}</h2>
            <p>${place.description || ''}</p>
            <p class="price">$${place.price} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(placeElement);
    });
}

checkAuthentication();
fetchPlaces();
