package aula5;

public class mesa {
        public int quantidadePernas;
        public String tipo;
        public String formaGeometrica;
    
        public mesa(){ }
    
        public boolean adicionarMesa(int qtdPernas, String tipo, String forma){
            if(this.setQuantidadePernas(qtdPernas) && this.setTipo(tipo)&& this.setForma(forma)){
                return true;
            }else{
                return false;
            }
        }
    
        public String mostrarMesa(){
            return "Mesa "+this.formaGeometrica+" com "+this.quantidadePernas+" pernas, do tipo "+this.tipo; 
        }
    
        private boolean setQuantidadePernas(int qtdPernas){
            if(isInterger(Integer.toString(qtdPernas))){
                this.quantidadePernas=qtdPernas;
                return true;
            }else{
                return false;
            }
        }
        private boolean setTipo(String tipo){
            if(isString(tipo)){
                this.tipo=tipo;
                return true;
            }else{
                return false;
            }
        }
        private boolean setForma(String forma){
            if(isString(forma)){
                this.formaGeometrica=forma;
                return true;
            }else{
                return false;
            }
        }
    
        private static boolean isInterger(String str){
            return str != null && str.matches("[0-9]*");
        }
        private static boolean isString(String str){
            return str != null && str.matches(".*[a-zA-Z]+.*");
        }

}
