const OVERLAY_ID = 'wapsa-overlay';

const DialogService = {
    registerDialog: (dialogId, buttonId) => {
        const dialogButton = document.getElementById(buttonId);
        const dialogOverlay = document.getElementById(OVERLAY_ID);
        const dialog = document.getElementById(dialogId);
        const body = document.getElementsByTagName('body')[0]
        const innerDialogClose = document.getElementById(`${dialogId}-close`);
        
        const openLoginDialog = () => {
            dialog.classList.add('wapsa-dialog-open');
            dialogOverlay.classList.add('wapsa-overlay-open');
            body.style.overflow = 'hidden';
        }
    
        const closeLoginDialog = () => {
            dialog.classList.remove('wapsa-dialog-open');
            dialogOverlay.classList.remove('wapsa-overlay-open');
            body.style.overflow = 'auto';
        }
    
        if (dialogButton) dialogButton.addEventListener('click', openLoginDialog, false);
        if (dialogOverlay) dialogOverlay.addEventListener('click', closeLoginDialog, false);
        if (innerDialogClose) innerDialogClose.addEventListener('click', closeLoginDialog, false);
    }
}
