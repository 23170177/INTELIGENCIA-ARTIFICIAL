import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class ArbolBinario<T> {

    protected NodoArbol<T> raiz;
    protected int tamanio;

    public ArbolBinario() {
        vaciar();
    }

    public ArbolBinario(T elementoRaiz, ArbolBinario<T> izquierdo, ArbolBinario<T> derecho) {
        if (elementoRaiz == null) {
            vaciar();
            return;
        }

        raiz = new NodoArbol<>(elementoRaiz);
        tamanio = 1;
        enlazarSubarbol(true, izquierdo);
        enlazarSubarbol(false, derecho);
    }

    private void enlazarSubarbol(boolean esIzquierdo, ArbolBinario<T> subarbol) {
        if (subarbol == null || subarbol.getRaiz() == null) {
            return;
        }

        if (esIzquierdo) {
            raiz.setIzquierdo(subarbol.getRaiz());
        } else {
            raiz.setDerecho(subarbol.getRaiz());
        }
        tamanio += subarbol.size();
    }

    public NodoArbol<T> getRaiz() {
        return raiz;
    }

    public void setRaiz(NodoArbol<T> raiz) {
        this.raiz = raiz;
    }

    public int size() {
        return tamanio;
    }

    public boolean isEmpty() {
        return raiz == null || tamanio == 0;
    }

    public void removeLeftSubtree() {
        if (isEmpty() || raiz.getIzquierdo() == null) {
            return;
        }
        tamanio -= raiz.getIzquierdo().numeroDeHijos() + 1;
        raiz.setIzquierdo(null);
    }

    public void removeRightSubtree() {
        if (isEmpty() || raiz.getDerecho() == null) {
            return;
        }
        tamanio -= raiz.getDerecho().numeroDeHijos() + 1;
        raiz.setDerecho(null);
    }

    public void removeAllElements() {
        vaciar();
    }

    private void vaciar() {
        raiz = null;
        tamanio = 0;
    }

    public boolean contains(T elemento) {
        return elemento != null && !isEmpty() && existe(raiz, elemento);
    }

    private boolean existe(NodoArbol<T> actual, T elemento) {
        if (actual == null) {
            return false;
        }
        if (elemento.equals(actual.getElemento())) {
            return true;
        }
        if (existe(actual.getIzquierdo(), elemento)) {
            return true;
        }
        return existe(actual.getDerecho(), elemento);
    }

    public Iterator<T> iteratorPreOrden() {
        List<T> recorrido = new LinkedList<>();
        recorrerPreOrden(raiz, recorrido);
        return recorrido.iterator();
    }

    private void recorrerPreOrden(NodoArbol<T> actual, List<T> recorrido) {
        if (actual == null) {
            return;
        }
        recorrido.add(actual.getElemento());
        recorrerPreOrden(actual.getIzquierdo(), recorrido);
        recorrerPreOrden(actual.getDerecho(), recorrido);
    }
}

