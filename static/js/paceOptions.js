paceOptions = {
    // Disable the 'elements' source
    elements: false,

    // Only show the progress on regular and ajax-y page navigation, not every request
    restartOnRequestAfter: 5,
    ajax: {
    	trackMethods: ['GET', 'POST', 'PUT', 'DELETE', 'REMOVE'],
    }
}