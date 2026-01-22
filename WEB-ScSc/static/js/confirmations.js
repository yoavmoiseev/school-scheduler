// Confirmation dialogs

const Confirmations = {
    show(title, message, callback) {
        const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('confirmationModal'));
        document.getElementById('confirmationMessage').textContent = message;
        
        const yesBtn = document.getElementById('confirmYes');
        const noBtn = document.getElementById('confirmNo');
        
        // Remove old listeners
        const newYesBtn = yesBtn.cloneNode(true);
        const newNoBtn = noBtn.cloneNode(true);
        yesBtn.parentNode.replaceChild(newYesBtn, yesBtn);
        noBtn.parentNode.replaceChild(newNoBtn, noBtn);
        
        // Default focus on NO button
        modal._element.addEventListener('shown.bs.modal', () => {
            newNoBtn.focus();
        });
        
        newYesBtn.addEventListener('click', () => {
            modal.hide();
            callback(true);
        });
        
        newNoBtn.addEventListener('click', () => {
            modal.hide();
            callback(false);
        });
        
        modal.show();
    },
    
    saveConfig(callback) {
        this.show(
            _('Confirm'),
            _('Are you sure you want to save the configuration? This will apply the changes.'),
            callback
        );
    },
    
    clearSchedules(callback) {
        this.show(
            _('Confirm'),
            _('Delete all schedules? This will remove all generated schedules but keep Teachers, Groups, and Subjects.'),
            callback
        );
    },
    
    deleteItem(itemName, callback) {
        const message = _('Are you sure you want to delete {ITEM}?').replace('{ITEM}', itemName);
        this.show(
            _('Confirm'),
            message,
            callback
        );
    },
    
    autofillSchedule(groupName, callback) {
        const message = _('AutoFill the schedule for GROUP_NAME? This will add lessons to empty slots while preserving any assigned lessons.').replace('GROUP_NAME', groupName);
        this.show(
            _('Confirm'),
            message,
            callback
        );
    }
};
