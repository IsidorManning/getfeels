// Global methods

/** 
  * Removes an element in a visually pleasing and smooth way.
  * @param {element} element - The element to remove
*/
function smoothDeleteElement(element) {
  // To make a visually pleasing deletion, we fade out the 
  // element before actually deleting it from the DOM.
  this.smoothlyFadeOut(element);
  // Remove element now that opacity of the element is 0.
  element.remove();
}

/**
  * Set's a timout for one quarter of a second before it sets some 
  * inputted element's opacity to 0. 
  * 
  * We assume the input-element has a set transition speed so that 
  * the overall effect becomes that the element smoothly fades out.
  * @param {element} element - The element whose opacity to change
*/
function smoothlyFadeOut(element) {
  setTimeout(() => {
    element.style.opacity = "0";
  }, 250);
}

/**
  * Set's a timout for one quarter of a second before it sets some 
  * inputted element's opacity to 1.
  * 
  * We assume the input-element has a set transition speed so that 
  * the overall effect becomes that the element smoothly fades in.
  * @param {element} element - The element whose opacity to change
*/
function smoothlyFadeIn(element) {
  setTimeout(() => {
    element.style.opacity = "1";
  }, 250);
}

/**
  * Checks for errors in sentiment analysis probabilities.
  * @param {string} negativesProba - The probability of negative sentiment.
  * @param {string} neutralsProba - The probability of neutral sentiment.
  * @param {string} positivesProba - The probability of positive sentiment.
  * @returns {boolean} True if all probabilities are empty strings, indicating an 
  * error; otherwise, false.
*/
function dataIsEmpty(negativesProba, neutralsProba, positivesProba) {
  if (negativesProba === '') {
    if (neutralsProba === '') {
      if (positivesProba === '') {
        return true
      }
    }
  }
  return false;
}

/**
  * This class is used for creating a pie chart with
  * the given probabilities from the predictions of the BERT model.
*/
class Chart {
  /**
    * Creates a new Chart instance.
    * @param {number} negativesProba - The percentege in decimal form of 
    * the comments that were classified as negative.
    * @param {number} neutralsProba - The percentege in decimal form of 
    * the comments that were classified as neutral.
    * @param {number} positivesProba - The percentege in decimal form of 
    * the comments that were classified as positive.
  */
  constructor(negativesProba, neutralsProba, positivesProba) {
    this.negatives = negativesProba;
    this.neutrals = neutralsProba;
    this.positives = positivesProba;

    // The container in which the pie chart will be positioned in.
    this.container = document.getElementById("content");
    
    // The label-specific colors for each type of probability outcome.
    //
    // Starting at the first element of the array, the order of goes 
    // from negatives, to neutrals, to positives.
    this.colors = ['#d20e0f', '#fe8100', '#00af12'];

    // The names of each of the labels in the pie chart. Their corresponding
    // probabilities in terms of percentege are also shown.
    //
    // Starting at the first element of the array, the order of goes 
    // from negatives, to neutrals, to positives.
    this.labelNames = [
      `Negative comments (${negativesProba * 100}%)`, 
      `Neutral commeents (${neutralsProba * 100}%)`, 
      `Positive comments (${positivesProba * 100}%)`,
    ];
  }

  // Creates a new pie chart element that is used to visualiuze the 
  // distribution of the probabilities. This elemnt gets appended
  // to the instance variable 'container'.
  showChart() {
    const pieChart = document.createElement("div"); 
    pieChart.className = "piechart";

    // We set opacity to 0 initially so that we later can smoothly 
    // fade the pie chart in by having a transition speed set and 
    // bringing up the opacity after we appended the element to the DOM.
    pieChart.style.opacity = "0";

    // Calculate the label's corresponding angle by multiplying the 
    // decimal probability by 360.
    const negativeAngle = this.negatives * 360;
    const neutralAngle = this.neutrals * 360;
    const positiveAngle = this.positives * 360;

    // Set the background image style of the pie chart element. What this
    // does is that it fills in a part of a circle with a certain color, based
    // on the its angle (the angle we just calculatd).
    const backgroundImageStyle = `conic-gradient(
      ${this.colors[0]} 0 ${negativeAngle}deg,
      ${this.colors[1]} 0 ${negativeAngle + neutralAngle}deg,
      ${this.colors[2]} 0 ${negativeAngle + neutralAngle + positiveAngle}deg
    );`;
    pieChart.style.cssText = "background-image: " + backgroundImageStyle;
    
    // Add the pie chart element to the DOM and then smoothly fade it in.
    this.container.appendChild(pieChart);
    smoothlyFadeIn(pieChart);
  }

  // Creates a list element of labels (or item elements)
  // which then gets appended to the instance variable 'container' 
  showLabels() {
    const labelsList = document.createElement("ul");
    labelsList.className = "labels-list";

    // We set opacity to 0 initially so that we later can smoothly 
    // fade the element in by having a transition speed set and 
    // bringing up the opacity after we appended the element to the DOM.
    labelsList.style.opacity = "0";

    // Iterate over the amount of labels which would be three:
    // negatives, neutrals, positives.
    //
    // Within each iteration, create a new item of the list representing
    // one label.
    for (let i = 0; i < 3; ++i) {
      const label = document.createElement("li");

      label.style.color = this.colors[i];
      label.innerHTML = this.labelNames[i];
      label.className = "labels-item font";

      labelsList.appendChild(label);
    }

    // Add the label elements to the DOM and then smoothly fade them in.
    this.container.appendChild(labelsList);
    smoothlyFadeIn(labelsList);
  }
}

/**
  * This class provided functionality for manipulating existing 
  * elements in the DOM and for creating new elements dynamically.
*/
class Screen {
  showLoadingScreen() {
    // Create the loading screen container element.
    const loadingScreenContainer = this.createLoadingScreenContainer();

    // Create the loading screen animation element.
    const loadingScreen = this.createLoadingScreen();
    
    // Append all of our newly created elements to the DOM. The "root
    // parent" is the main container which holds all content, 'content'.
    const body = document.getElementById("content");
    body.appendChild(loadingScreenContainer);
    loadingScreenContainer.appendChild(loadingScreen);
    
    smoothlyFadeIn(loadingScreenContainer);
  }

  /**
    * Creates a new loading screen container element.
    * @returns {element} The new loading screen container element
  */
  createLoadingScreenContainer() {
    // Create a div element and apply appropriate properties.  
    // This container will hold be the parent element
    // of the actual loading screen animation element.
    const loadingScreenContainer = document.createElement("div");
    // We set opacity to 0 initially so that we later can smoothly 
    // fade the element in by having a transition speed set and 
    // bringing up the opacity after we appended the element to the DOM.
    loadingScreenContainer.style.opacity = "0";
    loadingScreenContainer.id = "loading-screen";
    loadingScreenContainer.classList = "red loading-screen";

    return loadingScreenContainer;
  }

  /**
    * Creates a new loading screen element.
    * @returns {element} The new loading screen element
  */
  createLoadingScreen() {
    // Create a div element and apply appropriate properties.  
    // Notice that the div is not only an animation, but it also 
    // contains a paragraph, 'loadingScreenText'.
    const loadingScreen = document.createElement("div");
    loadingScreen.classList = "loader";
    const loadingScreenText = document.createElement("p");
    loadingScreenText.className = "font";
    loadingScreenText.innerHTML = "Analyzing... BERT is analyzing human emotions...";

    return loadingScreen;
  }
  
  deleteStartPage() {
    const startpageContainerElement = document.getElementById("startpage-container");
    smoothDeleteElement(startpageContainerElement);
  }

  deleteLoadingScreen() {
    const loadingScreenElement = document.getElementById("loading-screen");
    smoothDeleteElement(loadingScreenElement);
  }

  /**
    * Displays a warning message on the webpage.
    * @param {string} errorMessage - The warning message to be displayed.
  */
  handleAnyError(errorMessage) {
    // if the warning is empty, we return.
    if (errorMessage === '') return;
    else {
      const content = document.getElementById('content');
      // Create the paragraph that will hold the warning message.
      const error = document.createElement("p");
      // We set opacity to 0 initially so that we later can smoothly 
      // fade the element in by having a transition speed set and 
      // bringing up the opacity after we appended the element to the DOM.
      error.innerHTML = `Error: ${errorMessage}. Try again by
      clicking the button in the top right corner, or by refreshing the page.`;
      error.style.opacity = "0";
      error.classList = "font error";
      content.appendChild(error);
      
      smoothlyFadeIn(error);
    }
  }
}

// Error handling function that gets executed whenever the user would
// input a channel name that is not considered valid.
function displayError() {
  const inputElement = document.getElementById("input-form");
  inputElement.innerHTML = "Please enter a channel name";
}

// Asynchronous function that is responsible for handling the main logic
// of the program. This function gets called whenever a user submits 
// a form ('form'), containing the YouTube channel name that they wish 
// to analyze the viewer comment's sentiment of. 
const analyze = async () => {
  // Get the channel name that was inputted by the user in the 
  // input element with id 'channelNameInput'.
  const channelName = document.getElementById('channelNameInput').value;
  if (!channelName) {
    // Handle the case where a user did not enter any channel name and
    // submitted an empty string. 
    displayError();
    return;
  }

  // Create a new 'Screen' instance so that we can start manipulating 
  // the visual screen dynamically.
  const screen = new Screen();
  // Delete the start page after the user have entered a valid 
  // channel name.
  screen.deleteStartPage();
  // display the loading screen until the response has been fetched and
  // the predictions are back. 
  screen.showLoadingScreen();

  // Fetch the response using the 'fetch' API.
  const response = await fetch('/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ channel_name: channelName }),
  });
  const data = await response.json();
  // Extract the predictions from the fetched data.
  const { negatives, neutrals, positives, error } = data;


  if (!(dataIsEmpty(negatives, positives, neutrals))) {
    // Create a new 'Chart' instance so that we can prettily visualize the
    // distribution of the probabilities using a Pie Chart.
    const chart = new Chart(negatives, neutrals, positives);
    chart.showLabels(); // show the labels
    chart.showChart(); // Create and display the actual pie chart.
  } else {
    // If the data is empty, it indactes that there has been an error
    // that we now need to display an handle.
    screen.handleAnyError(error);
  }

  // Now we can delete the loading screen since the sentiment analyzis
  // has returned the predictions and since we have created a chart element
  // to visualize the data. 
  screen.deleteLoadingScreen();
}

// The main function which only should be called once 
// upon the DOM being successfully loaded.
function main() {
  // Get the form element in which the user inputs the name of their
  // YouTube channel
  const form = document.getElementById("input-form");

  form.onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    // Analyze the given data the user inputs whenever they submit
    // the form.
    analyze();
  };
}

document.addEventListener('DOMContentLoaded', main);
