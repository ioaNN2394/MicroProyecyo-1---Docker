document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    
    const orderBtn = document.getElementById('order-btn');
    orderBtn.addEventListener('click', placeOrder);
});

let productsData = [];
let cart = {}; // Objeto para el carrito: { productId: quantity }

async function loadProducts() {
    const response = await fetch('/api/products');
    if (!response.ok) {
        console.error("Error al cargar productos");
        return;
    }
    productsData = await response.json();
    const productListDiv = document.getElementById('product-list');
    productListDiv.innerHTML = ''; // Limpiar
    
    productsData.forEach(product => {
        const card = `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text">Precio: $${product.price}</p>
                        <p class="card-text">Disponibles: ${product.quantity}</p>
                        <button class="btn btn-success" onclick="addToCart(${product.id})" ${product.quantity === 0 ? 'disabled' : ''}>
                            ${product.quantity === 0 ? 'Agotado' : 'Añadir al Carrito'}
                        </button>
                    </div>
                </div>
            </div>
        `;
        productListDiv.innerHTML += card;
    });
}

function addToCart(productId) {
    const product = productsData.find(p => p.id === productId);
    
    // Verificar stock
    const currentQuantityInCart = cart[productId] || 0;
    if (currentQuantityInCart >= product.quantity) {
        alert('No puedes agregar más de este producto, stock no disponible.');
        return;
    }

    cart[productId] = (cart[productId] || 0) + 1;
    updateCartView();
}

function updateCartView() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = '';
    let total = 0;
    
    if (Object.keys(cart).length === 0) {
        cartItemsDiv.innerHTML = '<p>El carrito está vacío.</p>';
        document.getElementById('order-btn').disabled = true;
    } else {
        document.getElementById('order-btn').disabled = false;
    }

    for (const productId in cart) {
        const product = productsData.find(p => p.id === parseInt(productId));
        const quantity = cart[productId];
        total += product.price * quantity;
        
        cartItemsDiv.innerHTML += `
            <p>
                ${product.name} - Cantidad: ${quantity} - Subtotal: $${product.price * quantity}
            </p>
        `;
    }
    document.getElementById('cart-total').textContent = total.toFixed(2);
}

async function placeOrder() {
    if (Object.keys(cart).length === 0) {
        alert('Tu carrito está vacío.');
        return;
    }

    const orderProducts = Object.keys(cart).map(id => ({
        id: parseInt(id),
        quantity: cart[id]
    }));
    
    const orderData = {
        user_name: sessionStorage.getItem('username'),
        user_email: sessionStorage.getItem('email'),
        products: orderProducts
    };

    const response = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
    });

    if (response.ok) {
        alert('¡Pago exitoso! Orden creada correctamente.');
        cart = {}; // Limpiar carrito
        updateCartView();
        loadProducts(); // Recargar productos para ver stock actualizado
    } else {
        const result = await response.json();
        alert(`Error al crear la orden: ${result.message}`);
    }
}
