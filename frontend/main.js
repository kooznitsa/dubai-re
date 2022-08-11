let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')

if (token) {
    loginBtn.remove()
} else {
    logoutBtn.remove()
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'file:///C:/Users/Julia/Documents/p/code/tranio/dubai_re/frontend/login.html'
})



let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

let getProjects = () => {

    fetch(projectsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildProjects(data)
        })

}

let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects-wrapper')
    projectsWrapper.innerHTML = ''

    for (let i = 0; projects.length > i; i++) {
        let project = projects[i]

        let projectCard = `
                <div class="card mb-5">
                    <img class="card-img-top" src="http://127.0.0.1:8000${project.featured_image}" />
                    
                    <div class="card-body">
                        <h3 class="card-title">${project.highlights}</h3>
                        <p class="card-text">${project.amenities.substring(0, 150)}</p>
                    </div>
                
                </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
}


getProjects()