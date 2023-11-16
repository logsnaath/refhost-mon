/*
 * Author: Logu R<logu.rangasamy@suse.com>
 *
 */

document.addEventListener('DOMContentLoaded', function () {
    var sidebarLinks = document.querySelectorAll('.location-link');

    sidebarLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            sidebarLinks.forEach(function (otherLink) {
                otherLink.style.backgroundColor = '';
            });
            this.style.backgroundColor = "#4ddd3a";
        });
    });
});

function updateBannerTableHeaders(location, arch, product, version) {
    function setColor(elm){
        return `<span style="color:white"> ${elm || 'All'}</span>`;
    }

    // Get references to the bannertbl headers
    const locationHeader = document.getElementById('locationHeader');
    const archHeader = document.getElementById('archHeader');
    const productHeader = document.getElementById('productHeader');
    const versionHeader = document.getElementById('versionHeader');

    // Update the headers with the selected values
    locationHeader.innerHTML = `Location: ${setColor(location)}`;
    archHeader.innerHTML = `Arch: ${setColor(arch)}`;
    productHeader.innerHTML = `Product: ${setColor(product)}`;
    versionHeader.innerHTML = `Version: ${setColor(version)}`;
}

function resetFilters() {
    const selects = document.querySelectorAll('.sidebar select');
    selects.forEach(select => {
        select.value = '';
    });
    updateFilter();
}

function updateStatusElement(elementId, status) {
    const element = document.getElementById(elementId);
    if (element) {
        element.width = 25;
        element.height = 25;
        if (status === 'Up') {
            element.src = '/static/images/up.png';
            element.alt = 'Up';
        } else if (status === 'Down') {
            element.src = '/static/images/down.png';
            element.alt = 'Down';
        } else {
            element.src = '/static/images/loading.avif';
            element.alt = 'Checking...';
        }
    } else {
        console.log(elementId + " Not FOUND");
    }
}

function fetchStatus(location, arch, product, version) {
    fetch(`/status?location=${location}&arch=${arch}&product=${product}&version=${version}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                data.forEach(item => {
                    const hostname = item.hostname;
                    updateStatusElement(`icmp_image-${hostname}`, item.check_icmp_status);
                    updateStatusElement(`ssh_image-${hostname}`, item.check_ssh_status);
                });
            });
}

function insertCellText(row, textcont) {
    newCell = row.insertCell(-1);
    newCell.textContent = textcont;
}

function insertCellHtml(row, htmlcont) {
    newCell = row.insertCell(-1);
    newCell.innerHTML = htmlcont;
}

function insertHostInfo(sno, item) {
    table = document.getElementById("hostinfotbl");
    newRow = table.insertRow(-1);

    insertCellText(newRow, sno);
    insertCellText(newRow, item.hostname);
    insertCellText(newRow, item.arch);
    insertCellText(newRow, item.product);
    insertCellText(newRow, item.version);
    insertCellText(newRow, item.location);

    insertCellHtml(newRow, "<img id='icmp_image-"+item.hostname + "' src='/static/images/loading.gif' height=25 width=25 alt='Checking...'>");
    insertCellHtml(newRow, "<img id='ssh_image-"+item.hostname + "' src='/static/images/loading.gif' height=25 width=25 alt='Checking...'>");
}

function deleteRows(){
    var table = document.getElementById("hostinfotbl");
    for (var i = table.rows.length - 1; i > 0; i--) {
        table.deleteRow(i);
    }
}

function fetchAndDisplayHostsInfo(location, arch, product, version) {
    const allHosts = document.querySelectorAll('.host-row');
    allHosts.forEach(host => {
        const hostLocation = host.getAttribute('data-location');
        if (hostLocation === location || location === '') {
            host.style.display = 'table-row';
        } else {
            host.style.display = 'none';
        }
    });

    deleteRows();
    fetch(`/hostinfo?location=${location}&arch=${arch}&product=${product}&version=${version}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var i = 0;
            Object.keys(data).forEach(item => {
                i++
                insertHostInfo(i, data[item]);
            });
            fetchStatus(location, arch, product, version);
    });
}

function updateFilter() {
    const location = document.getElementById('locationFilter').value;
    const arch = document.getElementById('archFilter').value;
    const product = document.getElementById('productFilter').value;
    const version = document.getElementById('versionFilter').value;

    updateBannerTableHeaders(location, arch, product, version);
    fetchAndDisplayHostsInfo(location, arch, product, version);
}
updateFilter()

// Refresh the status every 300 seconds
//setInterval(updateStatus, 300000);
