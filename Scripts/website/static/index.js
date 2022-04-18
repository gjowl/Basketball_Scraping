//this function sends a really basic request to the backend to delete a note 
function deleteNote(noteId) {
    //sends a request to /delete-note endpoint
    fetch("/delete-note", {
      //post request
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      //reloads the window to the / page
      window.location.href = "/";
    });
  }