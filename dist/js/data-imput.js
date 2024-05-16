window.addEventListener('DOMContentLoaded', event => {

    const litepickerDateRange = document.getElementById('litepickerDateRange');
    if (litepickerDateRange) {
        new Litepicker({
            element: litepickerDateRange,
            singleMode: false,
            format: 'DD MMM, YYYY'
        });
    }



    const litepickerRangePlugin = document.getElementById('litepickerRangePlugin');
    if (litepickerRangePlugin) {
        new Litepicker({
            element: litepickerRangePlugin,
            numberOfMonths: 2,
            numberOfColumns: 2,
            format: 'DD MMM, YYYY',
        });
    }
});