document.addEventListener('DOMContentLoaded', () => {
    const username = sessionStorage.getItem('username');

    if (!username) {
        window.location.href = '/';
        return;
    }

    fetch(`/api/orders/user/${username}`)
        .then(response => response.json())
        .then(orders => {
            const container = document.getElementById('orders-container');
            container.innerHTML = '';

            if (orders.length === 0) {
                container.innerHTML = '<p>No has realizado ninguna orden todavía.</p>';
                return;
            }

            orders.forEach(order => {
                // Crear la lista de productos para esta orden
                let itemsHtml = '<ul class="list-group list-group-flush">';
                order.items.forEach(item => {
                    const itemPrice = parseFloat(item.price);
                    itemsHtml += `<li class="list-group-item">
                        ${item.name} - Cantidad: ${item.quantity} (a $${itemPrice.toFixed(2)} c/u)
                    </li>`;
                });
                itemsHtml += '</ul>';

                // Crear la tarjeta completa de la orden
                const orderCard = `
                    <div class="card mb-3">
                        <div class="card-header">
                            <strong>Orden #${order.id}</strong> - 
                            <span class="text-muted">${new Date(order.date).toLocaleString()}</span>
                        </div>
                        <div class="card-body">
                            ${itemsHtml}
                        </div>
                        <div class="card-footer">
                            <strong>Total: $${parseFloat(order.saleTotal).toFixed(2)}</strong>
                        </div>
                    </div>
                `;
                container.innerHTML += orderCard;
            });
        })
        .catch(error => {
            console.error('Error al cargar las órdenes:', error);
            const container = document.getElementById('orders-container');
            container.innerHTML = '<p>Error al cargar el historial de órdenes.</p>';
        });
});
