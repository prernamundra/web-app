let autocomplete;
let addressInput;
let latitude;
let longitude;

function initAutocomplete() {
  addressInput = document.querySelector("#input_addr");
  latitude = document.querySelector("#input_lat");
  longitude = document.querySelector("#input_long");
  latitude.style.display ="none";
  longitude.style.display ="none";
  // Create the autocomplete object, restricting the search predictions to
  // addresses in the US and Canada.
  autocomplete = new google.maps.places.Autocomplete(addressInput, {
    componentRestrictions: { country: ["in"] }
  });
  
  addressInput.focus();
  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
  // Get the place details from the autocomplete object.
  const place = autocomplete.getPlace();
  const lat = place.geometry.location.lat();
  const long = place.geometry.location.lng();;
  addressInput.value= place.formatted_address;
  latitude.value=lat;
  longitude.value=long;

}

google.maps.event.addDomListener(window, 'load', initialize); 
