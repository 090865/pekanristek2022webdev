const placeholder = document.querySelector('#data-output');

async function removeHandler(id) {
  await fetch(`http://localhost:8000/item/${id}`, {
    method: 'DELETE',
  });
  render();
}

async function editHandler(event, id) {
  event.preventDefault();
  const formElEdit = document.querySelector('.edit');
  const formData = new FormData(formElEdit);
  const data = Object.fromEntries(formData);
  console.log(id);
  console.log(data);
  await fetch(`http://localhost:8000/edit/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error));
  render();
}

function showEdit(event, id) {
  event.preventDefault()
  console.log(id);
  const editContainer = document.querySelector('.editContainer');
  const editForm = `  
    <form class="edit">
        <h2>Edit data</h2>
        input
        <input id='itempemasukanedit' name="itempemasukan" type="text" placeholder="Masukkan item pemasukan Anda" >
        <input id='pemasukanedit' name="pemasukan" type="text" placeholder="Masukkan dalam rupiah">
        <input id="itempengeluaranedit"  name="itempengeluaran" type="text" placeholder="Masukkan item pengeluaran Anda">
        <input id="pemgeluaranedit" name="pengeluaran" type="text" placeholder="Masukkan dalam rupiah">
        <button onClick="editHandler(event, this.id)" type="submitput" id=${id}>Submit data saya</button>
    </form>`;
  editContainer.innerHTML = editForm;
}

async function render() {
  await fetch('http://localhost:8000/items')
    .then(function (response) {
      return response.json();
    })
    .then(function (products) {
      let out = '';
      let total = 0;
      for (let product of products) {
        total += product.pemasukan;
        total -= product.pengeluaran;
        out += `
                <tr>
                    <td>${product.itempemasukan}
                        <button onClick="removeHandler(this.id)" style="padding: 5px; background-color: red; color: white;" id="${product.itempemasukan}">HAPUS</a>
                        <button onClick="showEdit(event, this.id)" style="padding: 5px; background-color: orange; color: white;" id="${product.itempemasukan}">EDIT</a>
                    </td>
                    <td>${product.pemasukan}</td>
                    <td>${product.itempengeluaran}</td>
                    <td>${product.pengeluaran}</td>
                </tr>
                `;
      }
      out += `<p>Total: ${total}</p>`;
      placeholder.innerHTML = out;
    });
}

async function simpanData() {
  const formData = new FormData(formEl);
  const data = Object.fromEntries(formData);
  console.log(data);

  await fetch('http://localhost:8000/items', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error));
}

const formEl = document.querySelector('.form');
formEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  await simpanData();
  render();
});

render();