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
                    <div class="card-body">
                        <a href="http://127.0.0.1:8000/project/${project.id}" target="_blank">
                            <h4 class="card-title">${project.highlights}</h4>
                        <a/>
                        <p class="card-text">PRICE: AED ${project.price}</p>
                        <p class="card-text">SURFACE: ${project.surface} sqf</p>
                        <p class="card-text">${project.amenities.substring(0, 300)}</p>
                    </div>
                
                </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
}


getProjects()