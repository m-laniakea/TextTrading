$(function(){

   var locations = [
          "University of Washington - Bothell",
          "University of Washington",
          "University of California - Berkeley",
          "University of Illinois - Urbana-Champaign",
          "University of Texas - Austin",
          "Georgia Institute of Technology",
          "Stanford University",
          "California Institute of Technology"
  ]

        
  $('#autoc').autocomplete({
    lookup: locations,
  });
  

});
