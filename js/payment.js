// PayPal integration
function initPayPalButton(planType) {
    const plans = {
        'basic': {
            price: '50.00',
            period: 'year',
            description: 'Basic Plan - Annual'
        },
        'pro': {
            price: '1000.00',
            period: 'year',
            description: 'Pro Plan - Annual'
        }
    };

    const plan = plans[planType];
    
    paypal.Buttons({
        style: {
            shape: 'rect',
            color: 'blue',
            layout: 'vertical',
            label: 'subscribe'
        },
        createSubscription: function(data, actions) {
            return actions.subscription.create({
                'plan_id': planType === 'basic' ? 'BASIC_PLAN_ID' : 'PRO_PLAN_ID', // Replace with your PayPal plan IDs
                'custom_id': 'mysticscape_' + planType,
                'subscriber': {
                    'email_address': 'wambuiraymond03@gmail.com'
                }
            });
        },
        onApprove: function(data, actions) {
            alert('Thank you for your subscription! You will receive an email with download instructions.');
            // Redirect to download page or show download link
            window.location.href = '/download.html?subscription=' + data.subscriptionID;
        }
    }).render('#paypal-button-' + planType);
}
