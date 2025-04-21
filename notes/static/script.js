document.addEventListener(
  "DOMContentLoaded",
  // once the page is loaded
  () => {
    console.log("DOMContentLoaded")
    document
      .querySelectorAll(".note>form>input")
      // on every input element inside the form inside the note class
      .forEach((element) => {
        // how to react on its change event
        element.addEventListener("change", (event) => {
          const done = element.checked
          const id = element.dataset.id
          console.log(JSON.stringify({ done }));
          // ask the API to update the note
          fetch(`/api/notes/${id}/done`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ done }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.ok) {
                console.log("ok")
              } else {
                console.log(data.status, data)
              }
            })
        })
      })
  },
)

let socket = io.connect(
  "http://" + document.domain + ":" + location.port);

  socket.on('notes_update', function(data) {
    const id_note = data.id_note;
    const done = data.done;
  
    document.querySelectorAll('input[type="checkbox"][data-id]').forEach((checkbox) => {
      if (checkbox.getAttribute('data-id') == id_note) {
        checkbox.checked = done;
      }
    });
  });