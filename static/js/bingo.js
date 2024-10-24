const socket = io();
function listarCartonesPremiados(){
  url = '/listarCartonePremiados'
  $.ajax({
    type: "POST",
    url: url,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()
          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
      $('#container').html(response)
      
    },
    error: function(error) {
      console.log(error);
    }

  });
  return false; 
}


function listaLetra(){
  url = '/listaLetra'
  $.ajax({
    type: "POST",
    url: url,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()
          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
      $('#container').html(response)
      },
      error: function(error) {
        console.log(error);
      }
  });
  return false; 
}


function listarCartones(){
  url = '/listarCartones'
  $.ajax({
    type: "POST",
    url: url,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()
          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
        $('#container').html(response)
      },
      error: function(error) {
        console.log(error);
      }
  });
  return false; 
}

function comprar(serialComprado){
  // Obtener elementos del DOM
var modal = document.getElementById('miModal');
var btnCerrar = document.getElementById('cerrarModal');
$('#serial1').val(serialComprado)
$('#serial').val(serialComprado)
$('#monto1').val('20,00 BS')
$('#monto').val('20')

modal.style.display = 'block';

// Asociar evento de clic al botón de cerrar
btnCerrar.onclick = function() {
  modal.style.display = 'none';
}

// Cerrar el modal si el usuario hace clic fuera de él
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}
}

function validarNumero(event) {
  var input = event.key;
  if (input === '' || isNaN(input)) {
    document.getElementById('mensajeValidacion').innerText = 'Por favor ingresa solo números';
  } else {
    document.getElementById('mensajeValidacion').innerText = '';
  }
}

function validarNumeroBanco(event) {
  var input = event.key;
  if (input === '' || isNaN(input)) {
    document.getElementById('mensajeValidacionBanco').innerText = 'Por favor ingresa solo números';
  } else {
    document.getElementById('mensajeValidacionBanco').innerText = '';
  }
}

function comprarCarton(){
  url = '/compraBoleto'
  Banco = $('#codigoBanco').val()
  referencia = $('#referencia').val()
  monto = $('#monto').val()
  serial = $('#serial').val()
  cedulaPremio = $('#cedulaPremio').val()
  bancoPremio = $('#bancoPremio').val()
  telefonoPremio = $('#telefonoPremio').val()

  dato ={
    "Banco": Banco,
    "serialBoleto":serial,
    "monto": monto,
    "referencia": referencia,
    'cedulaPremio': cedulaPremio,
    'bancoPremio': bancoPremio,
    'telefonoPremio': telefonoPremio
  }
  
  $.ajax({
    type: "POST",
    url: url,
    data:dato,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()

          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
          
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
      $('#container').html(response)
      // Hacer un elemento visible
      document.getElementById("validacionCompra").style.display = "block";
    },
    error: function(error) {
      console.log(error);
    }

  });
  return false; 

}

function salaJuego(){
  url = '/salaJuego'
  $.ajax({
    type: "POST",
    url: url,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()
          const b = Swal.getHtmlContainer().querySelector('b')
          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
            b.textContent = seconds
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
      $('#container').html(response)
      
    },
    error: function(error) {
      console.log(error);
    }
  });
  return false; 
}

//letra cantada 
function letraCantada(){
  url = '/letraCantada'
  $.ajax({
    type: "POST",
    url: url,
    beforeSend:function(){
      let timerInterval
      Swal.fire({
        title: '',
        html: 'Procesando.',
        timer: 5000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading()
          const b = Swal.getHtmlContainer().querySelector('b')
          timerInterval = setInterval(() => {
            const seconds = Math.ceil(Swal.getTimerLeft() / 1000) // Convertir milisegundos a segundos y redondear hacia arriba
            b.textContent = seconds
          }, 1000) // Actualizar cada segundo en lugar de cada 100 milisegundos
        },
        willClose: () => {
          clearInterval(timerInterval)
        }  
      })
    },
    success: function(response) {
      console.log(response)
      $('#container').html(response)
      
    },
    error: function(error) {
      console.log(error);
    }
  });
  return false; 
}


socket.emit('fecha', 'Fecha Actual');

socket.on('date',(msg) =>{
  document.getElementById('fecha').innerText = msg;
});

socket.emit('hora', 'Hora Actual');

socket.on('time',(msg) =>{
  document.getElementById('hora').innerText = msg;
});

socket.on('limpiarSala',(msg) =>{
  console.log(msg)
  salaJuego();
});

 
socket.on('culta',(msg) =>{
  document.getElementById('horaoculta').innerText = msg;
});

socket.on('inicio',(sorteoPendiente) =>{
  pote = document.getElementById('fecha').innerText;
  socket.emit('inicioSorteo', sorteoPendiente,pote);
});

socket.on('bingo',(msg) =>{
  $('#cantado').html(msg)
});

socket.on('resultadoLetraFecha',(msg) =>{
  console.log('Lista resultado Letra: ',msg['resultado']);

  const filaContenido = document.getElementById('fila-contenido');
  // Limpiar el contenido de la fila
  filaContenido.innerHTML = '';
  if(msg['resultado']!='Sin resultados'){
    msg.forEach(dato => {
    const columna = document.createElement('div');
    columna.className = 'col'; // Clase de Bootstrap para columnas

    // Crear un elemento de imagen
    const imagen = document.createElement('img');
    imagen.src = 'static/image/letras/' + dato[1] + '.png'; // Reemplaza con la nueva ruta de la imagen
    imagen.style.width = '60px'; // Definir el ancho de la imagen
    imagen.style.height = '40px'; // Mantener la proporción de la imagen
    // Agregar la imagen a la columna
    columna.appendChild(imagen);
    columna.innerHTML += `<p style="font-size:10px;">${dato[2]}</p>`;
    // Agregar la columna a la fila
    filaContenido.appendChild(columna);

    //const listaSorteo = document.createElement('div');
    // Personalizar el contenido de la columna
    //listaSorteo.innerHTML += `</strong> ${dato[2]}</strong>`;
    //columna.appendChild(listaSorteo);

    // Agregar la columna a la fila
    //filaContenido.appendChild(listaSorteo);
      
    console.log(dato);   
    });
  }
});

socket.on('lotto',(msg) =>{
  const imagen = document.getElementById('lotto');
  imagen.src = 'static\\image\\letras\\'+msg+'.png'; // Reemplaza con la nueva ruta de la imagen

  demo()

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function demo() {
    console.log("Inicio de la espera...");
    await sleep(120000); // Espera 20 segundos
    imagen.src = 'static\\image\\letra.gif'; // Reemplaza con la nueva ruta de la imagen
    console.log("¡2 segundos después!");
  }
  console.log(msg)
});

socket.on('bingo',(msg) =>{
  $('#cantado').html(msg)
});

socket.on('pote',(msg) =>{
  document.getElementById('pote').innerText = msg;
});

socket.on('boletoventa',(msg) =>{
  console.log(msg)
  document.getElementById('cartones').innerText = msg;
});


socket.on('agr',(msg) =>{
  $('#cantado').html(msg)
});

socket.on('sorteo',(msg) =>{
  console.log(msg)
  console.log(msg['montoPote'])
  document.getElementById('sorteo').innerText = msg['horaSorteo'];
  document.getElementById('pote').innerText = msg['montoPote'];
});


socket.on('message', (msg) => {
  console.log('Received message: ' + msg['numero']);
  $('#cantado').html(msg['numero'])
  var elemento = document.getElementById('cantado'); // Reemplaza 'miElemento' con el ID de tu elemento
  // Aplicar el subrayado al elemento
  elemento.style.textDecoration = 'underline';
  
  if(msg['numero']== 1){
     // Agregar una clase
    var miElemento = document.getElementById('1');
    miElemento.classList.add('esfera_seleccionada');
  }
 
  if(msg['numero']== 2){
    // Agregar una clase
    var miElemento = document.getElementById('2');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 3){
    // Agregar una clase
    var miElemento = document.getElementById('3');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 4){
    // Agregar una clase
    var miElemento = document.getElementById('4');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 5){
    // Agregar una clase
    var miElemento = document.getElementById('5');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 6){
    // Agregar una clase
   var miElemento = document.getElementById('6');
   miElemento.classList.add('esfera_seleccionada');
 }

  if(msg['numero']== 7){
    // Agregar una clase
    var miElemento = document.getElementById('7');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 8){
    // Agregar una clase
    var miElemento = document.getElementById('8');
    miElemento.classList.add('esfera_seleccionada');
  }

  if(msg['numero']== 9){
    // Agregar una clase
   var miElemento = document.getElementById('9');
   miElemento.classList.add('esfera_seleccionada');
 }

 if(msg['numero']== 10){
  // Agregar una clase
 var miElemento = document.getElementById('10');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 11){
  // Agregar una clase
 var miElemento = document.getElementById('11');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 12){
  // Agregar una clase
 var miElemento = document.getElementById('12');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 13){
  // Agregar una clase
 var miElemento = document.getElementById('13');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 14){
  // Agregar una clase
 var miElemento = document.getElementById('14');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 15){
  // Agregar una clase
 var miElemento = document.getElementById('15');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 16){
  // Agregar una clase
 var miElemento = document.getElementById('16');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 17){
  // Agregar una clase
 var miElemento = document.getElementById('17');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 18){
  // Agregar una clase
 var miElemento = document.getElementById('18');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 19){
  // Agregar una clase
 var miElemento = document.getElementById('19');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 20){
  // Agregar una clase
 var miElemento = document.getElementById('20');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 21){
  // Agregar una clase
 var miElemento = document.getElementById('21');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 22){
  // Agregar una clase
 var miElemento = document.getElementById('22');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 23){
  // Agregar una clase
 var miElemento = document.getElementById('23');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 24){
  // Agregar una clase
 var miElemento = document.getElementById('24');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 25){
  // Agregar una clase
 var miElemento = document.getElementById('25');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 26){
  // Agregar una clase
 var miElemento = document.getElementById('26');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 27){
  // Agregar una clase
 var miElemento = document.getElementById('27');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 28){
  // Agregar una clase
 var miElemento = document.getElementById('28');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 29){
  // Agregar una clase
 var miElemento = document.getElementById('29');
 miElemento.classList.add('esfera_seleccionada');
}


if(msg['numero']== 30){
  // Agregar una clase
 var miElemento = document.getElementById('30');
 miElemento.classList.add('esfera_seleccionada');
}


if(msg['numero']== 31){
  // Agregar una clase
 var miElemento = document.getElementById('31');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 32){
  // Agregar una clase
 var miElemento = document.getElementById('32');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 33){
  // Agregar una clase
 var miElemento = document.getElementById('33');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 34){
  // Agregar una clase
 var miElemento = document.getElementById('34');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 35){
  // Agregar una clase
 var miElemento = document.getElementById('35');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 36){
  // Agregar una clase
 var miElemento = document.getElementById('36');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 37){
  // Agregar una clase
 var miElemento = document.getElementById('37');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 38){
  // Agregar una clase
 var miElemento = document.getElementById('38');
 miElemento.classList.add('esfera_seleccionada');
}


if(msg['numero']== 39){
  // Agregar una clase
 var miElemento = document.getElementById('39');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 40){
  // Agregar una clase
 var miElemento = document.getElementById('40');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 41){
  // Agregar una clase
 var miElemento = document.getElementById('41');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 42){
  // Agregar una clase
 var miElemento = document.getElementById('42');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 43){
  // Agregar una clase
 var miElemento = document.getElementById('43');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 44){
  // Agregar una clase
 var miElemento = document.getElementById('44');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 45){
  // Agregar una clase
 var miElemento = document.getElementById('45');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 46){
  // Agregar una clase
 var miElemento = document.getElementById('46');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 47){
  // Agregar una clase
 var miElemento = document.getElementById('47');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 48){
  // Agregar una clase
 var miElemento = document.getElementById('48');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 49){
  // Agregar una clase
 var miElemento = document.getElementById('49');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 50){
  // Agregar una clase
 var miElemento = document.getElementById('50');
 miElemento.classList.add('esfera_seleccionada');
}


if(msg['numero']== 51){
  // Agregar una clase
 var miElemento = document.getElementById('51');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 52){
  // Agregar una clase
 var miElemento = document.getElementById('52');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 53){
  // Agregar una clase
 var miElemento = document.getElementById('53');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 54){
  // Agregar una clase
 var miElemento = document.getElementById('54');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 55){
  // Agregar una clase
 var miElemento = document.getElementById('55');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 56){
  // Agregar una clase
 var miElemento = document.getElementById('56');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 57){
  // Agregar una clase
 var miElemento = document.getElementById('57');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 58){
  // Agregar una clase
 var miElemento = document.getElementById('58');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 59){
  // Agregar una clase
 var miElemento = document.getElementById('59');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 60){
  // Agregar una clase
 var miElemento = document.getElementById('60');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 61){
  // Agregar una clase
 var miElemento = document.getElementById('61');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 62){
  // Agregar una clase
 var miElemento = document.getElementById('62');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 63){
  // Agregar una clase
 var miElemento = document.getElementById('63');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 64){
  // Agregar una clase
 var miElemento = document.getElementById('64');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 65){
  // Agregar una clase
 var miElemento = document.getElementById('65');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 66){
  // Agregar una clase
 var miElemento = document.getElementById('66');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 67){
  // Agregar una clase
 var miElemento = document.getElementById('67');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 68){
  // Agregar una clase
 var miElemento = document.getElementById('68');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 69){
  // Agregar una clase
 var miElemento = document.getElementById('69');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 70){
  // Agregar una clase
 var miElemento = document.getElementById('70');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 71){
  // Agregar una clase
 var miElemento = document.getElementById('71');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 72){
  // Agregar una clase
  var miElemento = document.getElementById('72');
  miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 73){
  // Agregar una clase
 var miElemento = document.getElementById('73');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 74){
  // Agregar una clase
 var miElemento = document.getElementById('74');
 miElemento.classList.add('esfera_seleccionada');
}

if(msg['numero']== 75){
  // Agregar una clase
 var miElemento = document.getElementById('75');
 miElemento.classList.add('esfera_seleccionada');
}

});