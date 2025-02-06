let selectedCourse = '';

function selectCourse(course) {
    selectedCourse = course;
    localStorage.setItem('selectedCourse', selectedCourse);

    window.location.href = `/${course}`;
}
