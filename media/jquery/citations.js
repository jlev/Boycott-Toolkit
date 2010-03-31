$().ready(function() { 
      //show-hide citation section
      $(".citation_link").click(function() {
        $(this).next().toggle();
        return false;
        //to stop browser default action, scrolling to hidden anchor
      });
      
      //enable autocompletes
      $(".author_div").children('input').autocomplete("/autocomplete/info.source/author/entries.json", { multiple: false });
      $(".title_div").children('input').autocomplete("/autocomplete/info.source/name/entries.json", { multiple: false });
      
      //save the citations
      $(".citation_save_link").click(function() {
        //get the data from the previous fields
        var theAuthor = $(this).siblings('.author_div').children('input').val();
        var theTitle = $(this).siblings('.title_div').children('input').val();
        var theDate = $(this).siblings('.date_div').children('input').val();
        var theURL = $(this).siblings('.url_div').children('input').val();
        var theField = $(this).parent().siblings('.citation_list').attr('id');
        
        if (theAuthor == "" && theTitle == "" && theDate == "") {
          //no data entered
          return false;
        }
        
        //pack the data into a js object
        var cite = {
         field:theField,
         author:theAuthor,
         title:theTitle,
         date:theDate,
         url:theURL
        };
        
        //save it to the hidden field
        citations_json = $("#id_citations_json").val();
        if(citations_json) citations = $.evalJSON(citations_json);
        else citations = new Array();
        citations.push(cite);
        $("#id_citations_json").val($.toJSON(citations));
        
        //save a textual representation to the visible div
        var citeVisible = "<li>" + cite.author + " <i>" + cite.title + "</i> " + cite.date
        if (theURL) {citeVisible += '<a href="'+theURL+' target="_blank"</a>'}
        $(this).parent().siblings('.citation_list').append(citeVisible);
        
        //clear the fields
        $(this).siblings('.author_div').children('input').val("");
        $(this).siblings('.title_div').children('input').val("");
        $(this).siblings('.date_div').children('input').val("");
        $(this).siblings('.url_div').children('input').val("");
        
        //hide the div
        $(this).parent().hide();
      });
      
      //on form submission, serialize global array to hidden input field
      $(":submit").click(function() {
        $("#id_citations_json").val();
        return true; //let django do the rest
      });
 });