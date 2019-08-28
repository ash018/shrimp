/**
 * Created by shakil.ahammad on 8/28/2019.
 */




Array.prototype.checkArrayItem = function () {
    for (var i = 0; i < this.length; i++) {
        for(var j = 0; j< this.length; j++){
            if (this[i] == this[j] && i != j){
                return true;
            }
        }
    }
    return false;
}