public class NodoArbol<T> {

    private T dato;
    private NodoArbol<T> hijoIzq;
    private NodoArbol<T> hijoDer;

    public NodoArbol(T dato) {
        this(dato, null, null);
    }

    public NodoArbol(T dato, NodoArbol<T> hijoIzq, NodoArbol<T> hijoDer) {
        this.dato = dato;
        this.hijoIzq = hijoIzq;
        this.hijoDer = hijoDer;
    }

    public T getElemento() {
        return dato;
    }

    public void setElemento(T dato) {
        this.dato = dato;
    }

    public NodoArbol<T> getIzquierdo() {
        return hijoIzq;
    }

    public void setIzquierdo(NodoArbol<T> hijoIzq) {
        this.hijoIzq = hijoIzq;
    }

    public NodoArbol<T> getDerecho() {
        return hijoDer;
    }

    public void setDerecho(NodoArbol<T> hijoDer) {
        this.hijoDer = hijoDer;
    }

    public boolean esHoja() {
        return hijoIzq == null && hijoDer == null;
    }

    public int numeroDeHijos() {
        int total = 0;

        if (hijoIzq != null) {
            total += hijoIzq.numeroDeHijos() + 1;
        }
        if (hijoDer != null) {
            total += hijoDer.numeroDeHijos() + 1;
        }

        return total;
    }
}
