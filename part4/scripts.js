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
        placeElement.dataset.price = place.price;

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

function filterPlaces() {
    const selectedPrice = document.getElementById('price-filter').value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach((placeCard) => {
        const placePrice = parseFloat(placeCard.dataset.price);

        if (selectedPrice === 'all') {
            placeCard.style.display = 'block';
        } else {
            const maxPrice = parseFloat(selectedPrice);

            if (placePrice <= maxPrice) {
                placeCard.style.display = 'block';
            } else {
                placeCard.style.display = 'none';
            }
        }
    });
}

document.getElementById('price-filter').addEventListener('change', filterPlaces);

checkAuthentication();
fetchPlaces();
