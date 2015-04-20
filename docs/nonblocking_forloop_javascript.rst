Non-Blocking For Loop in Javascript
======

Let’s say you are iterating over an array and manipulating the DOM per array element. If your array is large enough, you may have a situation where repeated manipulation of the DOM events takes enough time to throw a ‘script unresponsive’ error.

The best way to solve this would be to optimize your iteration loop so that the iteration will complete in a set amount of time, but this is not always possible.

One way to get around this would be to use setTimeout to defer each DOM manipulation action.

This has the advantage of remaining ‘non-blocking’ so that the user’s browser will still be responsive as the loop actions are being completed in the background.

.. code-block:: javascript

    var loadingImageUrl = '"/static/img/loader.gif"';  
    var spin_css = {  
        'background-image': 'url(' + loadingImageUrl + ')',
        'background-repeat': 'no-repeat',
    };
    $(this).css(spin_css);
    var items = new Array();  
    var el = this;

    // add elements in 'non-blocking' fashion,
    // by using setTimeout per dom manipulation.
    var items_added = 0;  
    function doLoop(i){  
        doDomStuff(items[i]);
        if (i < items.length) {
            setTimeout(function() { doLoop(i+1); }, 50); 
        } else {
            items_added = 1;
        }
    };
    doLoop(0);

    // check if items_added loop is complete, if so, stop spinner
    var clearMe = setInterval(function() {
        if (items_added === 1) {
            setTimeout(function() { 
                var nospin_css = {
                    'background-image': 'none',
                    'background-repeat': 'no-repeat',
                }; 
                $(el).css(nospin_css); }, 200);
            clearSpinnerInterval();
        };
    },100);
    function clearSpinnerInterval(){ clearInterval(clearMe); }
