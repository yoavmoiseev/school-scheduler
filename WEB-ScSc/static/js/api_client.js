// API Client for School Scheduler

const API = {
    baseURL: '',
    
    async get(url) {
        try {
            const response = await fetch(this.baseURL + url);
            if (response.status === 401) {
                window.location.href = '/login';
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET error:', error);
            throw error;
        }
    },
    
    async post(url, data) {
        try {
            const response = await fetch(this.baseURL + url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (response.status === 401) {
                window.location.href = '/login';
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                // try to parse JSON error body so callers can handle structured errors
                try {
                    const errObj = await response.json();
                    return errObj;
                } catch (parseErr) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            }
            return await response.json();
        } catch (error) {
            console.error('API POST error:', error);
            throw error;
        }
    },
    
    async put(url, data) {
        try {
            const response = await fetch(this.baseURL + url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (response.status === 401) {
                window.location.href = '/login';
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API PUT error:', error);
            throw error;
        }
    },
    
    async delete(url, data = null) {
        try {
            const options = {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            if (data) {
                options.body = JSON.stringify(data);
            }
            const response = await fetch(this.baseURL + url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API DELETE error:', error);
            throw error;
        }
    }
};
