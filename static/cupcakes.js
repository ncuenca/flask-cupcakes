"use strict"

const $cupcakesList = $("#cupcakes-list");
const $newCupcakeFlavor = $("#new-cupcake-flavor");
const $newCupcakeSize = $("#new-cupcake-size");
const $newCupcakeRating = $("#new-cupcake-rating");
const $newCupcakeImage = $("#new-cupcake-image");

/**
 * Gets submitted cupcake values and calls functions to add/display
 * new cupcake
 */
function handleCupcakeSubmit(evt) {
    evt.preventDefault();

    const flavor = $newCupcakeFlavor.val();
    const size = $newCupcakeSize.val();
    const rating = $newCupcakeRating.val();
    const image = $newCupcakeImage.val();

    addCupcake(flavor, size, rating, image);
    appendCupcakeToHTML(flavor, size, rating);
}

/**
 * Takes in cupcake values and adds it to database
 */
async function addCupcake(flavor, size, rating, image) {
    const response = await axios({
        url: `/api/cupcakes`,
        method: "POST",
        data: {  flavor, size, rating, image }});
};

/**
 * Takes in cupcake values and adds it to HTML
 */
function appendCupcakeToHTML(flavor, size, rating) {
    $cupcakesList.append(`<li>${flavor} ${size} ${rating}</li>`)
};


$("#submit-cupcake").click(handleCupcakeSubmit);