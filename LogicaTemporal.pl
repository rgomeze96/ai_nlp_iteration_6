indiceDemanda("Procesador",0.2).
getCostoProducto("Procesador",1600).
tasaDeVentaPorTiempoProducto("Procesador",0.2).
timepoMaximoEnInventario("Procesador",30).
valorMinimoDeDemanda("Procesador",3).

indiceDemanda("Board",0.4).
getCostoProducto("Board",1300).
tasaDeVentaPorTiempoProducto("Board",0.3).
timepoMaximoEnInventario("Board",20).
valorMinimoDeDemanda("Board",2).

indiceDemanda("Ram",0.3).
getCostoProducto("Ram",1200).
tasaDeVentaPorTiempoProducto("Ram",0.3).
timepoMaximoEnInventario("Ram",40).
valorMinimoDeDemanda("Ram",3).

indiceDemanda("Fuente",0.5).
getCostoProducto("Fuente",1400).
tasaDeVentaPorTiempoProducto("Fuente",0.5).
timepoMaximoEnInventario("Fuente",60).
valorMinimoDeDemanda("Fuente",4).


analizarInventario(Producto, Cantidad, Presupuesto) :- 
    getCostoProducto(Producto,X), X * Cantidad =< Presupuesto,
    tasaDeVentaPorTiempoProducto(Producto, Y),
    timepoMaximoEnInventario(Producto,T), Cantidad*Y =< T, 
    indiceDemanda(Producto,I), valorMinimoDeDemanda(Producto,M), I =< M.
    
reabastecerProducto(Producto, Cantidad, Presupuesto) :- 
    analizarInventario(Producto,Cantidad,Presupuesto),
    getCostoProducto(Producto,X),
    R is Presupuesto - (X*Cantidad),
    write(' Compramos el producto '),
    write(Producto),
    write(' con una cantidad de '),
    write(Cantidad),
    write(' presupuesto restante '),
    write(R).